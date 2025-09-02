# VotePro - Render Deployment Guide

## 🚀 Quick Deployment Steps

### 1. **Prepare Your Repository**

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit for VotePro"

# Push to GitHub
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/votepro.git
git push -u origin main
```

### 2. **Deploy on Render**

1. **Go to [render.com](https://render.com)** and sign up
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure deployment:**

   **Basic Settings:**

   - **Name:** `votepro` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### 3. **Environment Variables**

In Render dashboard, add these environment variables:

**Required:**

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
```

**Email (Optional but recommended):**

```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

**Database (Auto-configured by Render):**

- Render will automatically provide `DATABASE_URL` if you add a PostgreSQL database

### 4. **Add PostgreSQL Database (Recommended)**

1. In your Render service dashboard
2. Click "Environment" tab
3. Click "Add Database"
4. Choose "PostgreSQL"
5. Render will automatically set `DATABASE_URL`

## 🔧 **Production Features**

### ✅ What Works Out of the Box:

- ✅ **Auto-scaling**
- ✅ **HTTPS/SSL certificates**
- ✅ **Custom domains**
- ✅ **Automatic deployments on git push**
- ✅ **Built-in monitoring**
- ✅ **PostgreSQL database**
- ✅ **Email functionality**
- ✅ **All polling features**

### 🎯 **Free Tier Limits:**

- ✅ **750 hours/month** (enough for small projects)
- ✅ **500MB RAM**
- ✅ **PostgreSQL database included**
- ⚠️ **Sleeps after 15 minutes of inactivity** (wakes up automatically)

## 🛠 **Post-Deployment Setup**

### 1. **Initialize Database**

After first deployment, your database tables will be created automatically.

### 2. **Configure Email (Optional)**

- Use Gmail App Passwords for email functionality
- Set up in Environment Variables section

### 3. **Custom Domain (Optional)**

- Add your domain in Render dashboard
- Configure DNS records as instructed

## 🚨 **Important Notes**

1. **Database:**

   - SQLite works for development
   - PostgreSQL automatically used in production

2. **Environment Variables:**

   - Never commit `.env` file to git
   - Use Render's Environment Variables instead

3. **Email Setup:**
   - Gmail requires App Passwords (not regular password)
   - Enable 2FA first, then generate App Password

## 📱 **Testing Your Deployment**

1. **Your app will be available at:** `https://your-app-name.onrender.com`
2. **Test all features:**
   - User registration
   - Email verification
   - Poll creation
   - Voting with OTP
   - View results

## 🔄 **Updates & Maintenance**

- **Auto-deploy:** Push to GitHub → Automatic deployment
- **Manual deploy:** Use Render dashboard
- **Logs:** Available in Render dashboard
- **Monitoring:** Built-in health checks

## 💡 **Pro Tips**

1. **Keep it alive:** Use a service like UptimeRobot to ping your app every 15 minutes
2. **Custom domain:** Much more professional than .onrender.com
3. **Database backups:** Render handles this automatically
4. **Scaling:** Upgrade plan if you get more traffic

## 🆘 **Troubleshooting**

**App won't start?**

- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure requirements.txt is correct

**Email not working?**

- Verify Gmail App Password
- Check MAIL_USERNAME and MAIL_PASSWORD variables
- Ensure 2FA is enabled on Gmail

**Database errors?**

- Render auto-creates tables on first run
- Check DATABASE_URL is set
- Verify PostgreSQL addon is connected
