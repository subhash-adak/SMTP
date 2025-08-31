# 📧 SMTP Configuration & Testing System

**Developed by: Subhash**

A professional SMTP testing system that sends automated daily emails to verify email configuration and connectivity. Perfect for testing Gmail SMTP settings and monitoring email delivery.

## 🌟 Features

- ✅ **Automated Daily Emails** - Sends test emails every 24 hours
- ⚡ **Real-time Testing** - Manual test email trigger
- 📊 **System Monitoring** - Health checks and status reports  
- 🔒 **Secure Configuration** - Environment variable based setup
- 🌐 **Web Interface** - Beautiful dashboard for monitoring
- ☁️ **Cloud Ready** - Optimized for Render deployment

## 📁 Project Structure

```
SMTP/
├── app.py                 # Main Flask application
├── email_service.py       # SMTP service functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone 
cd smtp-testing-system
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

TEST_EMAIL_1=recipient1@gmail.com
TEST_EMAIL_2=recipient2@gmail.com  
TEST_EMAIL_3=recipient3@gmail.com

APP_NAME=SMTP Testing System by Subhash
ENVIRONMENT=development
DEBUG=True
```

### 3. Run Locally
```bash
python app.py
```

Visit: `http://localhost:5000`

## ☁️ Render Deployment

### 1. Environment Variables
Set these in Render dashboard:
```
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-app-password
MAIL_DEFAULT_SENDER = your-email@gmail.com
TEST_EMAIL_1 = recipient1@gmail.com
TEST_EMAIL_2 = recipient2@gmail.com
TEST_EMAIL_3 = recipient3@gmail.com
APP_NAME = SMTP Testing System by Subhash
ENVIRONMENT = production
DEBUG = False
```

### 2. Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment**: `Python 3`

## 📧 Gmail Setup

### 1. Enable 2-Factor Authentication
- Go to Google Account settings
- Enable 2FA

### 2. Generate App Password
- Google Account → Security → App Passwords
- Generate password for "Mail"
- Use this password in `MAIL_PASSWORD`

### 3. Alternative: Less Secure Apps
- Enable "Less secure app access" (not recommended)

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Home dashboard |
| `/health` | GET | System health check |
| `/test-smtp` | GET | Send test emails now |
| `/smtp-status` | GET | Scheduler status |
| `/config` | GET | View configuration |

## 📊 System Behavior

### Daily Schedule
- **Frequency**: Every 24 hours
- **Recipients**: 3 configured email addresses
- **Content**: Date, time, greetings, system status
- **First Run**: 30 seconds after app start

### Email Timing
- **Per Email**: 3-5 seconds (normal for Gmail SMTP)
- **Total Time**: ~10-15 seconds for all 3 emails
- **Delay**: 1 second between emails to avoid rate limits

## 🔧 Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Check Gmail app password
   - Verify 2FA is enabled
   - Ensure credentials are correct

2. **"Connection timeout"**
   - Check internet connectivity
   - Verify firewall allows port 587
   - Try different SMTP server

3. **"Name not defined" errors**
   - Ensure all imports are correct
   - Check function definitions

### Debug Mode
Set `DEBUG=True` in environment for detailed logs.

## 📈 Monitoring

### Health Check Response
```json
{
  "status": "healthy",
  "service": "SMTP Testing System", 
  "developer": "Subhash",
  "smtp": {
    "scheduler_running": true,
    "test_recipients": 3
  }
}
```

### Log Format
```
2025-08-31 22:59:35 - INFO - ✅ Email sent successfully to recipient@gmail.com
```

## 🔒 Security

- ✅ Environment variables for sensitive data
- ✅ No hardcoded credentials in code
- ✅ .gitignore prevents credential leaks
- ✅ TLS encryption for email transmission

## 📝 License

This project is created for SMTP testing purposes.

## 👨‍💻 Developer

**Subhash** - SMTP Configuration & Testing Specialist

---

## 📞 Support

For issues or questions about this SMTP testing system, check the logs and health endpoints first.

### Quick Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally  
python app.py

# Check logs (when deployed)
# View in Render dashboard logs section
```

## 🚀 Version History

- **v1.0** - Initial SMTP testing system
- **v1.1** - Added Render deployment support
- **v1.2** - Fixed timing issues and reduced email frequency

---
**⭐ SMTP Testing System by Subhash - Reliable Email Configuration Testing**
