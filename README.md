# VotePro - Online Voting and Polling Platform

A comprehensive Flask-based online voting platform that demonstrates advanced web development skills while solving real-world polling needs for communities, organizations, and institutions.

## 🚀 Features

### Core Functionality
- **Multi-topic Polling**: Create polls across various categories (Technology, Workplace, Education, etc.)
- **Anonymous Voting**: Secure voting system that maintains voter privacy
- **Real-time Results**: Interactive charts with live updates every 30 seconds
- **Email/OTP Verification**: Two-factor authentication to prevent duplicate voting
- **User Management**: Complete registration, login, and email verification system

### Advanced Features
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Interactive Charts**: Pie charts and bar charts using Chart.js
- **Poll Management**: Create, edit, activate/deactivate, and delete polls
- **Export Functionality**: Download poll results in JSON format
- **Social Sharing**: Share polls on Twitter, Facebook, and WhatsApp
- **Real-time Analytics**: Live vote counting and percentage calculations
- **Security**: CSRF protection, password hashing, session management

### Security & Privacy
- **Anonymous Voting**: Votes are anonymized using secure tokens
- **Email Verification**: OTP-based verification for account creation and voting
- **Duplicate Prevention**: One vote per user per poll enforcement
- **Secure Authentication**: Bcrypt password hashing and session management
- **Input Validation**: Server-side and client-side form validation

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Bcrypt**: Password hashing
- **Flask-Mail**: Email service integration
- **SQLite**: Database (development)

### Frontend
- **Bootstrap 5**: CSS framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icons
- **Vanilla JavaScript**: Interactive functionality

### Database Schema
```sql
Users: id, email, password_hash, is_verified, created_at
Polls: id, title, description, category, creator_id, created_at, deadline, is_active
Poll_Options: id, poll_id, option_text
Votes: id, poll_id, option_id, voter_token, created_at
Verification_Tokens: id, user_id, token, token_type, expires_at, poll_id
```

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation Steps

1. **Clone or download the project files**
```bash
# Create project directory
mkdir votepro && cd votepro
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file or modify the configuration in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

5. **Initialize the database**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
votepro/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage with poll listings
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── verify_email.html # Email verification page
│   ├── create_poll.html  # Poll creation form
│   ├── view_poll.html    # Poll viewing and voting page
│   └── my_polls.html     # User's poll management page
└── voting_platform.db    # SQLite database (created on first run)
```

## 🎯 Usage Guide

### For Users
1. **Register**: Create an account with email verification
2. **Browse Polls**: View active polls on the homepage
3. **Vote**: Select an option and verify with OTP sent to your email
4. **View Results**: See real-time results with interactive charts

### For Poll Creators
1. **Create Polls**: Use the intuitive poll creation form
2. **Manage Polls**: Activate/deactivate polls as needed
3. **View Analytics**: Track votes and engagement metrics
4. **Share Polls**: Use built-in social sharing features
5. **Export Data**: Download poll results for analysis

## 🔧 Development Features

### Demo Mode
- Email verification codes are displayed in the browser console
- OTP codes are generated and shown in console logs
- Perfect for development and demonstration purposes

### Customization Options
- **Categories**: Add new poll categories in the create poll form
- **Themes**: Modify CSS variables in `base.html` for custom styling
- **Email Integration**: Configure Flask-Mail for production email sending
- **Database**: Switch from SQLite to PostgreSQL for production

## 🚀 Resume Value

This project demonstrates:

### Technical Skills
- **Full-stack Development**: Complete Flask application with frontend and backend
- **Database Design**: Normalized schema with proper relationships
- **Security Implementation**: Authentication, authorization, and data protection
- **API Development**: RESTful endpoints for AJAX functionality
- **Real-time Features**: Live updates and interactive components

### Problem-Solving
- **Real-world Application**: Addresses actual need for digital polling
- **User Experience**: Intuitive interface with responsive design
- **Scalability**: Modular design that can handle growing user base
- **Security Focus**: Implements industry-standard security practices

### Professional Skills
- **Code Organization**: Clean, maintainable, and well-documented code
- **Version Control Ready**: Structured for Git workflow
- **Production Considerations**: Error handling and validation
- **Testing Ready**: Modular design facilitates unit testing

## 🔒 Security Features

- **Password Security**: Bcrypt hashing with salt
- **Session Management**: Secure session handling
- **CSRF Protection**: Built-in Flask CSRF protection
- **Input Validation**: Server-side validation for all forms
- **Anonymous Voting**: Voter identity protection through tokenization
- **Rate Limiting**: OTP and verification code timing controls

## 🌐 Production Deployment

For production deployment:

1. **Environment Variables**: Use environment variables for sensitive data
2. **Database**: Migrate to PostgreSQL or MySQL
3. **Email Service**: Configure with SendGrid, Mailgun, or AWS SES
4. **HTTPS**: Enable SSL/TLS encryption
5. **Reverse Proxy**: Use Nginx or Apache
6. **WSGI Server**: Deploy with Gunicorn or uWSGI

## 📈 Potential Extensions

- **Advanced Analytics**: Detailed voting patterns and demographics
- **Real-time Notifications**: WebSocket integration for live updates
- **Mobile App**: React Native or Flutter companion app
- **Social Authentication**: OAuth integration with Google, Facebook
- **Advanced Poll Types**: Ranked choice, multiple selection options
- **Moderation Tools**: Content filtering and admin controls

## 📄 License

This project is created for educational and portfolio purposes. Feel free to use it as a reference for your own projects.

---

**VotePro** - Demonstrating professional Flask development skills through a practical, feature-rich voting platform that solves real-world problems while showcasing technical expertise.