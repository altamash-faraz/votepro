from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import secrets
import os
from functools import wraps
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration - Updated for production
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production database (PostgreSQL, MySQL, etc.)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting_platform.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Validate email configuration
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print("WARNING: Email credentials not configured. Check your .env file.")
    print("Emails will fall back to console output.")

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    polls = db.relationship('Poll', backref='creator', lazy=True)
    verification_tokens = db.relationship('VerificationToken', backref='user', lazy=True)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    deadline = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    options = db.relationship('PollOption', backref='poll', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='poll', lazy=True, cascade='all, delete-orphan')

class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='option', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'), nullable=False)
    voter_token = db.Column(db.String(64), nullable=False)  # For anonymity
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(6), nullable=False)
    token_type = db.Column(db.String(20), nullable=False)  # 'email_verify' or 'vote_otp'
    expires_at = db.Column(db.DateTime, nullable=False)
    poll_id = db.Column(db.Integer, nullable=True)  # For vote OTP tokens

# Helper Functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_token():
    return str(random.randint(100000, 999999))

def make_timezone_aware(dt):
    """Convert a naive datetime to timezone-aware UTC datetime if needed"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # If datetime is naive, assume it's UTC
        return dt.replace(tzinfo=UTC)
    return dt

def send_verification_email(user_email, token, token_type):
    """Send email with verification token"""
    if token_type == 'email_verify':
        subject = 'VotePro - Email Verification'
        body = f'''Welcome to VotePro!

Your email verification code is: {token}

Please enter this code to complete your registration.

This code expires in 15 minutes.'''
    else:  # vote_otp
        subject = 'VotePro - Voting OTP'
        body = f'''Your voting OTP code is: {token}

Please enter this code to cast your vote.

This code expires in 5 minutes.'''
    
    # Debug: Check email configuration
    print(f"\n=== EMAIL DEBUG INFO ===")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD configured: {'Yes' if app.config.get('MAIL_PASSWORD') else 'No'}")
    print(f"Attempting to send to: {user_email}")
    print("========================\n")
    
    try:
        # Send actual email
        msg = Message(subject, recipients=[user_email])
        msg.body = body
        mail.send(msg)
        
        print(f"\n✅ EMAIL SENT SUCCESSFULLY ✅")
        print(f"To: {user_email}")
        print(f"Subject: {subject}")
        print("===============================\n")
        
    except Exception as e:
        # Detailed error information
        print(f"\n❌ EMAIL FAILED ❌")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        print(f"Recipient: {user_email}")
        print(f"Subject: {subject}")
        print(f"\n📧 CONSOLE FALLBACK:")
        print(f"Code: {token}")
        print("===================\n")
        
        # Re-raise the exception so we can see it in the web interface too
        raise e

# Routes
@app.route('/')
def index():
    # Get all active polls and filter for valid deadline in Python to handle timezone conversion
    all_polls = Poll.query.filter(Poll.is_active == True).all()
    polls = [poll for poll in all_polls if make_timezone_aware(poll.deadline) > datetime.now(UTC)]
    categories = db.session.query(Poll.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    # Get poll statistics
    poll_stats = []
    for poll in polls:
        vote_count = Vote.query.filter_by(poll_id=poll.id).count()
        poll_stats.append({
            'poll': poll,
            'vote_count': vote_count
        })
    
    return render_template('index.html', poll_stats=poll_stats, categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))
        
        # Create new user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        # Generate verification token
        token = generate_token()
        verification = VerificationToken(
            user_id=user.id,
            token=token,
            token_type='email_verify',
            expires_at=datetime.now(UTC) + timedelta(minutes=15)
        )
        db.session.add(verification)
        db.session.commit()
        
        # Send verification email
        try:
            send_verification_email(email, token, 'email_verify')
            flash('Registration successful! Check your email for verification code.', 'success')
        except Exception as e:
            flash(f'Registration successful! However, email sending failed. Your verification code is: {token}', 'warning')
            print(f"Email error during registration: {e}")
        
        session['pending_verification'] = user.id
        return redirect(url_for('verify_email'))
    
    return render_template('register.html')

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if 'pending_verification' not in session:
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        token = request.form['token']
        user_id = session['pending_verification']
        
        verification = VerificationToken.query.filter_by(
            user_id=user_id,
            token=token,
            token_type='email_verify'
        ).first()
        
        if verification and make_timezone_aware(verification.expires_at) > datetime.now(UTC):
            user = User.query.get(user_id)
            user.is_verified = True
            db.session.delete(verification)
            db.session.commit()
            
            session.pop('pending_verification', None)
            session['user_id'] = user.id
            flash('Email verified successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid or expired verification code.', 'danger')
    
    return render_template('verify_email.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not user.is_verified:
                flash('Please verify your email first.', 'warning')
                return redirect(url_for('verify_email'))
            
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/create-poll', methods=['GET', 'POST'])
@login_required
def create_poll():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M')
        
        # Create poll
        poll = Poll(
            title=title,
            description=description,
            category=category,
            creator_id=session['user_id'],
            deadline=deadline
        )
        db.session.add(poll)
        db.session.commit()
        
        # Add poll options
        options = request.form.getlist('options[]')
        for option_text in options:
            if option_text.strip():
                option = PollOption(poll_id=poll.id, option_text=option_text.strip())
                db.session.add(option)
        
        db.session.commit()
        flash('Poll created successfully!', 'success')
        return redirect(url_for('view_poll', poll_id=poll.id))
    
    return render_template('create_poll.html')

@app.route('/poll/<int:poll_id>')
def view_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    
    # Check if poll is still active
    if not poll.is_active or make_timezone_aware(poll.deadline) < datetime.now(UTC):
        flash('This poll is no longer active.', 'warning')
    
    # Get voting results
    results = []
    total_votes = Vote.query.filter_by(poll_id=poll_id).count()
    
    for option in poll.options:
        vote_count = Vote.query.filter_by(poll_id=poll_id, option_id=option.id).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'option': option,
            'count': vote_count,
            'percentage': round(percentage, 1)
        })
    
    # Check if poll is still active for voting
    is_poll_active_for_voting = poll.is_active and make_timezone_aware(poll.deadline) > datetime.now(UTC)
    
    return render_template('view_poll.html', 
                         poll=poll, 
                         results=results, 
                         total_votes=total_votes,
                         is_poll_active_for_voting=is_poll_active_for_voting)

@app.route('/vote/<int:poll_id>', methods=['POST'])
@login_required
def initiate_vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    
    # Check if poll is active
    if not poll.is_active or make_timezone_aware(poll.deadline) < datetime.now(UTC):
        return jsonify({'success': False, 'message': 'Poll is no longer active'})
    
    # Check if user already voted
    user = User.query.get(session['user_id'])
    existing_votes = Vote.query.filter_by(poll_id=poll_id).all()
    
    # Generate voting token for this session
    voting_token = secrets.token_hex(16)
    session[f'voting_token_{poll_id}'] = voting_token
    
    # Generate OTP
    otp = generate_token()
    verification = VerificationToken(
        user_id=session['user_id'],
        token=otp,
        token_type='vote_otp',
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        poll_id=poll_id
    )
    db.session.add(verification)
    db.session.commit()
    
    # Send OTP
    try:
        send_verification_email(user.email, otp, 'vote_otp')
        message = 'OTP sent to your email. Please verify to cast your vote.'
    except Exception as e:
        message = f'Email sending failed. Your OTP code is: {otp}'
        print(f"Email error during voting: {e}")
    
    return jsonify({
        'success': True,
        'message': message,
        'poll_id': poll_id
    })

@app.route('/verify-vote', methods=['POST'])
@login_required
def verify_vote():
    poll_id = request.json['poll_id']
    option_id = request.json['option_id']
    otp = request.json['otp']
    
    # Verify OTP
    verification = VerificationToken.query.filter_by(
        user_id=session['user_id'],
        token=otp,
        token_type='vote_otp',
        poll_id=poll_id
    ).first()
    
    if not verification or make_timezone_aware(verification.expires_at) < datetime.now(UTC):
        return jsonify({'success': False, 'message': 'Invalid or expired OTP'})
    
    # Check if voting token exists
    voting_token = session.get(f'voting_token_{poll_id}')
    if not voting_token:
        return jsonify({'success': False, 'message': 'Voting session expired'})
    
    # Check if already voted with this token
    existing_vote = Vote.query.filter_by(poll_id=poll_id, voter_token=voting_token).first()
    if existing_vote:
        return jsonify({'success': False, 'message': 'You have already voted in this poll'})
    
    # Cast vote
    vote = Vote(
        poll_id=poll_id,
        option_id=option_id,
        voter_token=voting_token
    )
    db.session.add(vote)
    db.session.delete(verification)
    db.session.commit()
    
    # Clear voting token
    session.pop(f'voting_token_{poll_id}', None)
    
    return jsonify({'success': True, 'message': 'Vote cast successfully!'})

@app.route('/api/poll-results/<int:poll_id>')
def poll_results_api(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    
    results = []
    total_votes = Vote.query.filter_by(poll_id=poll_id).count()
    
    for option in poll.options:
        vote_count = Vote.query.filter_by(poll_id=poll_id, option_id=option.id).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'option_text': option.option_text,
            'count': vote_count,
            'percentage': round(percentage, 1)
        })
    
    return jsonify({
        'poll_title': poll.title,
        'total_votes': total_votes,
        'results': results
    })

@app.route('/my-polls')
@login_required
def my_polls():
    polls = Poll.query.filter_by(creator_id=session['user_id']).order_by(Poll.created_at.desc()).all()
    current_time = datetime.now(UTC)
    
    poll_stats = []
    for poll in polls:
        vote_count = Vote.query.filter_by(poll_id=poll.id).count()
        poll_deadline = make_timezone_aware(poll.deadline)
        poll_stats.append({
            'poll': poll,
            'vote_count': vote_count,
            'is_active': poll.is_active and poll_deadline > current_time,
            'is_expired': poll_deadline < current_time,
            'days_left': (poll_deadline - current_time).days if poll_deadline > current_time else 0
        })
    
    return render_template('my_polls.html', poll_stats=poll_stats, current_time=current_time)

@app.route('/toggle-poll/<int:poll_id>')
@login_required
def toggle_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    
    if poll.creator_id != session['user_id']:
        flash('You can only modify your own polls.', 'danger')
        return redirect(url_for('my_polls'))
    
    poll.is_active = not poll.is_active
    db.session.commit()
    
    status = 'activated' if poll.is_active else 'deactivated'
    flash(f'Poll {status} successfully!', 'success')
    return redirect(url_for('my_polls'))

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)