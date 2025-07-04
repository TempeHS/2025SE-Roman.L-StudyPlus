import time
import random
from datetime import datetime
from urllib.parse import urlparse
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user
import userManagement as dbHandler
from userManagement import User
from src import password_hashing as psh
from src.config import app_log
from src.session_state import logout_required

auth_login_bp = Blueprint('auth_login', __name__)

def is_safe_url(target):
    '''
    Prevent open redirects
    '''
    allowed_urls = ['/', '/dashboard', '/index.html']
    parsed_url = urlparse(target)
    if parsed_url.netloc == '' and parsed_url.path in allowed_urls:
        return True
    return False

@auth_login_bp.route("/index.html", methods=["GET", "POST"])
@logout_required
def login():
    '''
    Authentication portal
    '''
    if request.method == "GET" and request.args.get("url"):
        target = request.args.get('url', '').strip()
        if is_safe_url(target):
            return redirect(target, code=302)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = dbHandler.retrieveUsers(email)
        if user and psh.verifyPassword(password, user[2]):
            user_obj = User(user[0], user[1], user[3], user[4], user[5], user[6])
            login_user(user_obj)
            time.sleep(random.uniform(0.1, 0.2))
            app_log.info("Successful login: %s", email)
            dbHandler.updateLastActivity(user[0])
            return redirect("/dashboard")

        time.sleep(random.uniform(0.1, 0.2))
        app_log.warning("Failed login attempt: %s | %s | %s",
                        email, request.remote_addr, datetime.now())
        flash("Invalid credentials.", "error")
    return redirect(url_for('index'))
