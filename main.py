# Standard Library Imports
import os
import ssl
from datetime import datetime, timedelta # Date and time
from urllib.parse import urlparse # URL parsing

# Third-Party Imports
from flask import Flask, redirect, render_template, request, session, url_for, flash, g
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter # Rate limiter
from flask_limiter.util import get_remote_address # Rate limiter
from flask_login import LoginManager, logout_user # Login manager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Local Application Imports
from src import session_state as sst
from src.security import init_security

# auth_routes imports
from src.auth_routes.signup import auth_signup_bp
from src.auth_routes.login import auth_login_bp
from src.auth_routes.form import auth_form_bp
from src.auth_routes.user import auth_user_bp
from src.auth_routes.dashboard import auth_dashboard_bp
from src.auth_routes.profile import auth_profile_bp

# Database functions
import userManagement as dbHandler

load_dotenv()

app = Flask(__name__)
init_security(app)

@app.before_request
def generate_nonce():
    '''
    Bypass CSP headers
    '''
    g.nonce = os.urandom(16).hex()

# CSRF
app.secret_key =  os.getenv('secret_key')
csrf = CSRFProtect(app)

scheduler = BackgroundScheduler()
scheduler.add_job(dbHandler.deleteUserByInactivity, 'interval', days=1)  # Run daily
scheduler.start()

# 30d expiration
app.permanent_session_lifetime = timedelta(days=30)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)

# Default rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "100 per hour"],
    storage_uri="memory://",
)

# Rate limit exceeded handler
@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Rate limit exceeded. Please try again later.", "error")
    return redirect(url_for('index'))

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login.login"

@login_manager.user_loader
def load_user(user_id):
    '''
    Load user by IDs
    '''
    return dbHandler.getUserById(user_id)

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self' 'unsafe-inline'",
        "script-src": "'self' 'unsafe-inline'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'"
    }
)

# Pages
@sst.logout_required
def index():
    '''
    Landing page when user is not logged in
    '''
    return render_template("/index.html")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    '''
    Privacy policy page
    '''
    return render_template("/privacy.html")

def is_safe_url(target):
    '''
    Check if the target URL is safe to redirect to
    '''
    allowed_urls = ['/', '/dashboard', '/index.html']
    parsed_url = urlparse(target)
    if parsed_url.netloc == '' and parsed_url.path in allowed_urls:
        return True
    return False

# Website blueprint
app.register_blueprint(auth_signup_bp)
app.register_blueprint(auth_login_bp)
app.register_blueprint(auth_form_bp)
app.register_blueprint(auth_user_bp)
app.register_blueprint(auth_dashboard_bp)
app.register_blueprint(auth_profile_bp)

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    '''
    Report CSP violations
    '''
    app.logger.critical(request.data.decode())
    return "done"

@app.before_request
def check_session_timeout():
    '''
    Session timeout check, 30 minutes
    '''
    if 'user_id' in session:
        last_activity = session.get('last_activity')
        if last_activity and datetime.now() - last_activity > timedelta(minutes=30):
            logout_user()
            return redirect(url_for('login'))
        session['last_activity'] = datetime.now()

## SSL Encryption
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certs/certificate.pem', 'certs/privatekey.pem')

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, ssl_context=None) # 'context' for HTTPS, SSL
