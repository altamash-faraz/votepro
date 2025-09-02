# Email Setup Instructions for VotePro

## Quick Setup Guide

### 1. Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Google account:

   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**:

   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Copy the generated 16-character password

3. **Update .env file**:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-gmail@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

### 2. Other Email Providers

#### Outlook/Hotmail:

```
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

#### Yahoo Mail:

```
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

### 3. Testing

1. Update your `.env` file with real credentials
2. Restart the Flask application
3. Register a new user or try voting to test email delivery

### 4. Troubleshooting

- **"Email failed" message**: Check your credentials in .env
- **"Less secure app access"**: Use App Passwords instead of regular passwords
- **Firewall issues**: Ensure port 587 is not blocked
- **Authentication failed**: Double-check username and password

### 5. Security Notes

- Never commit the `.env` file to version control
- Use App Passwords instead of regular passwords
- Consider using environment variables in production
- The `.env` file is already in `.gitignore` for security

## Current Status

✅ Email sending is now enabled
✅ Fallback to console if email fails
✅ Environment variables for security
✅ Support for multiple email providers
