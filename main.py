# Standard Library Imports
import os
import ssl
from datetime import datetime, timedelta # Date and time
from urllib.parse import urlparse # URL parsing

# Third-Party Imports
from flask import Flask, redirect, render_template, request, session, url_for, jsonify, flash, g
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter # Rate limiter
from flask_limiter.util import get_remote_address # Rate limiter
from flask_login import LoginManager, logout_user, login_required, current_user # Login manager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Local Application Imports
from src import session_state as sst # Custom modules
from src.security import init_security

# auth_routes imports
from src.auth_routes.signup import auth_bp
from src.auth_routes.login import auth_login_bp
from src.auth_routes.form import auth_form_bp
from src.auth_routes.user import auth_user_bp

import userManagement as dbHandler # Database functions

load_dotenv()

app = Flask(__name__)
init_security(app)

@app.before_request
def generate_nonce():
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

@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Rate limit exceeded. Please try again later.", "error")
    return redirect(url_for('index'))

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    ALLOWED_URLS = ['/', '/dashboard', '/index.html']
    parsed_url = urlparse(target)
    if parsed_url.netloc == '' and parsed_url.path in ALLOWED_URLS:
        return True
    return False

app.register_blueprint(auth_bp)

app.register_blueprint(auth_login_bp)

app.register_blueprint(auth_form_bp)

app.register_blueprint(auth_user_bp)

@app.route("/dashboard.html", methods=["GET", "POST"])
@login_required
def dashboard():
    todos = dbHandler.getTodos(current_user.id)
    for todo in todos:
        due = todo.get('due_date')
        if due:
            # Convert string to datetime if needed
            if isinstance(due, str):
                try:
                    due_dt = datetime.fromisoformat(due)
                except ValueError:
                    due_dt = datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
            else:
                due_dt = due
            todo['days_left'] = (due_dt.date() - datetime.now().date()).days
            todo['due_date_obj'] = due_dt
        else:
            todo['days_left'] = None
            todo['due_date_obj'] = None
    return render_template("dashboard.html", todos=todos)

@app.route("/delete_todo/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id):
    dbHandler.deleteTodo(current_user.id, todo_id)
    return redirect(url_for("dashboard"))

@app.route("/complete_todo/<int:todo_id>", methods=["POST"])
@login_required
def complete_todo(todo_id):
    dbHandler.statusTodo(current_user.id, todo_id)
    return redirect(url_for("dashboard"))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    '''
    Logout for logged in
    '''
    logout_user()
    flash("You have been logged out.", "info")
    return redirect('/index.html')

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
def checkSessionTimeout():
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
