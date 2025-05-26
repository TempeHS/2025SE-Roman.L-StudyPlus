from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import html
from datetime import datetime
from src import sanitize_and_validate as sv
import userManagement as dbHandler
from src.config import app_log

auth_form_bp = Blueprint('auth_form', __name__)

@auth_form_bp.route("/form.html", methods=["GET", "POST"])
@login_required
def form():
    '''
    Form page for posting, login required
    '''
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        due_date = request.form["due_date"]
        label = request.form["labels"]

        if not sv.validateLog(title, body):
            return redirect(url_for('form.form'))
        safe_title = html.escape(title)
        safe_body = sv.sanitizeLog(body)
        safe_due_date = html.escape(due_date)
        safe_label = html.escape(label)

        user_id = current_user.id
        user = dbHandler.getUserById(user_id)
        fullname = f"{user.firstname} {user.lastname}"
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        dbHandler.addTodo(safe_title, safe_body, fullname, user_id, current_date, safe_due_date, safe_label)
        app_log.info("New log created by %s: %s", user_id, title)
        return redirect(url_for('dashboard'))
    return render_template("/form.html")