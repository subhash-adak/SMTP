# from flask import Flask, jsonify, render_template_string
# import os
# from dotenv import load_dotenv

# # Import SMTP service
# from email_service import init_mail_service, start_smtp_scheduler, send_test_emails, get_smtp_health,get_current_time

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'smtp-testing-by-subhash-2025'

# # Initialize SMTP service
# init_mail_service(app)

# @app.route('/', methods=['GET', 'HEAD'])
# def home():
#     """Home page"""
#     template = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>SMTP Testing System by Subhash</title>
#         <style>
#             body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
#             .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
#             h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
#             .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
#             .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
#             .btn:hover { background: #0056b3; }
#             ul { list-style-type: none; padding: 0; }
#             li { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #007bff; }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>📧 SMTP Configuration & Testing System</h1>
            
#             <div class="info">
#                 <h3>👨‍💻 Developed by: Subhash</h3>
#                 <p>✅ System Status: Active and Running on Render</p>
#                 <p>🔧 Purpose: SMTP Configuration Testing</p>
#                 <p>📅 Sends automated test emails every 24 hours</p>
#             </div>

#             <h3>🛠️ System Features:</h3>
#             <ul>
#                 <li>📧 Automated daily SMTP testing</li>
#                 <li>📊 System status reporting</li>
#                 <li>🔍 Email delivery monitoring</li>
#                 <li>⚡ Real-time testing capabilities</li>
#             </ul>

#             <h3>🎯 Quick Actions:</h3>
#             <a href="/health" class="btn">System Health</a>
#             <a href="/test-smtp" class="btn">Send Test Emails Now</a>
#             <a href="/smtp-status" class="btn">SMTP Status</a>
#             <a href="/config" class="btn">View Configuration</a>

#             <div class="info">
#                 <small>🌐 Deployed on Render Cloud | ⏰ Running 24/7 | 🔒 Secure SMTP Configuration</small>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     return render_template_string(template)

# @app.route('/health')
# def health_check():
#     """Health check endpoint"""
#     try:
#         smtp_status = get_smtp_health()
#         return jsonify({
#             "status": "healthy",
#             "service": "SMTP Testing System",
#             "developer": "Subhash",
#             "smtp": smtp_status
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "unhealthy", 
#             "error": str(e)
#         }), 500

# @app.route('/test-smtp')
# def test_smtp_now():
#     """Send test emails immediately"""
#     try:
#         count = send_test_emails()
#         now = get_current_time()
#         return jsonify({
#             "status": "success",
#             "message": f"✅ Test emails sent to {count} recipients",
#             "developer": "Subhash",
#             "timestamp": now.strftime('%Y-%m-%d %H:%M:%S IST')
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "error": str(e)
#         }), 500

# @app.route('/smtp-status', methods=['GET', 'HEAD'])
# def smtp_status():
#     """Get SMTP system status"""
#     status = get_smtp_health()
#     return jsonify(status)

# @app.route('/config')
# def show_config():
#     """Show SMTP configuration (without sensitive data)"""
#     return jsonify({
#         "smtp_server": os.getenv('MAIL_SERVER'),
#         "smtp_port": os.getenv('MAIL_PORT'),
#         "use_tls": os.getenv('MAIL_USE_TLS'),
#         "sender_email": os.getenv('MAIL_DEFAULT_SENDER'),
#         "test_recipients": [
#             os.getenv('TEST_EMAIL_1'),
#             os.getenv('TEST_EMAIL_2'),
#             os.getenv('TEST_EMAIL_3')
#         ],
#         "app_name": os.getenv('APP_NAME'),
#         "environment": os.getenv('ENVIRONMENT'),
#         "configured_by": "Subhash"
#     })

# if __name__ == '__main__':
#     # Start SMTP testing scheduler
#     start_smtp_scheduler(app)
    
#     # Run Flask app
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')

from flask import Flask, jsonify, render_template_string
import os
from dotenv import load_dotenv

# Import SMTP service
from email_service import init_mail_service, start_smtp_scheduler, send_test_emails, get_smtp_health, get_current_time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smtp-testing-by-subhash-2025'

# Initialize SMTP service
init_mail_service(app)

# Start SMTP scheduler immediately when app loads (for gunicorn)
with app.app_context():
    start_smtp_scheduler(app)

@app.route('/', methods=['GET', 'HEAD'])
def home():
    """Home page"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SMTP Testing System by Subhash</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
            .btn:hover { background: #0056b3; }
            ul { list-style-type: none; padding: 0; }
            li { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #007bff; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .status.running { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .status.stopped { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📧 SMTP Configuration & Testing System</h1>
            
            <div class="info">
                <h3>👨‍💻 Developed by: Subhash</h3>
                <p>✅ System Status: Active and Running on Render</p>
                <p>📧 Purpose: SMTP Configuration Testing</p>
                <p>⏰ Sends automated test emails every 90 seconds</p>
                <p>🌐 Service URL: <code>https://smtp-cd3p.onrender.com</code></p>
            </div>

            <h3>🛠️ System Features:</h3>
            <ul>
                <li>📧 Automated 90-second SMTP testing</li>
                <li>📊 System status reporting</li>
                <li>📝 Email delivery monitoring</li>
                <li>⚡ Real-time testing capabilities</li>
                <li>🔄 Self-pinging to prevent sleep</li>
            </ul>

            <h3>🎯 Quick Actions:</h3>
            <a href="/health" class="btn">System Health</a>
            <a href="/test-smtp" class="btn">Send Test Emails Now</a>
            <a href="/smtp-status" class="btn">SMTP Status</a>
            <a href="/config" class="btn">View Configuration</a>

            <div class="info">
                <small>🌐 Deployed on Render Cloud | ⏰ Running 24/7 | 🔒 Secure SMTP Configuration</small>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        smtp_status = get_smtp_health()
        return jsonify({
            "status": "healthy",
            "service": "SMTP Testing System",
            "developer": "Subhash",
            "smtp": smtp_status,
            "service_url": "https://smtp-cd3p.onrender.com"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy", 
            "error": str(e)
        }), 500

@app.route('/test-smtp')
def test_smtp_now():
    """Send test emails immediately"""
    try:
        count = send_test_emails()
        now = get_current_time()
        return jsonify({
            "status": "success",
            "message": f"✅ Test emails sent to {count} recipients",
            "developer": "Subhash",
            "timestamp": now.strftime('%Y-%m-%d %H:%M:%S IST'),
            "type": "manual_test"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/smtp-status', methods=['GET', 'HEAD'])
def smtp_status():
    """Get SMTP system status"""
    status = get_smtp_health()
    return jsonify(status)

@app.route('/config')
def show_config():
    """Show SMTP configuration (without sensitive data)"""
    return jsonify({
        "smtp_server": os.getenv('MAIL_SERVER'),
        "smtp_port": os.getenv('MAIL_PORT'),
        "use_tls": os.getenv('MAIL_USE_TLS'),
        "sender_email": os.getenv('MAIL_DEFAULT_SENDER'),
        "test_recipients": [
            os.getenv('TEST_EMAIL_1'),
            os.getenv('TEST_EMAIL_2'),
            os.getenv('TEST_EMAIL_3')
        ],
        "app_name": os.getenv('APP_NAME'),
        "environment": os.getenv('ENVIRONMENT'),
        "configured_by": "Subhash",
        "service_url": "https://smtp-cd3p.onrender.com",
        "auto_scheduler": "90 seconds interval"
    })

if __name__ == '__main__':
    # This block only runs in local development
    # Start SMTP testing scheduler (already started above for gunicorn)
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')
