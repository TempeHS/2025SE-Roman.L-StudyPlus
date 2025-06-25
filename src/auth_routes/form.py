import html
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import userManagement as dbHandler
from src import sanitize_and_validate as sv
from src.config import app_log

auth_form_bp = Blueprint('auth_form', __name__)

@auth_form_bp.route("/form", methods=["GET", "POST"])
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

        if not sv.validateLog(title, body, due_date, label):
            flash("An error occurred while trying to complete your to-do. Please try again.", "error")
            return redirect(url_for('auth_form.form'))
        safe_title = html.escape(title)
        safe_due_date = html.escape(due_date)
        safe_label = html.escape(label)
        safe_body = sv.sanitizeLog(body)

        user_id = current_user.id
        user = dbHandler.getUserById(user_id)
        fullname = f"{user.firstname} {user.lastname}"
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        dbHandler.addTodo(safe_title, safe_body,
        fullname, user_id, current_date, safe_due_date, safe_label)
        app_log.info("New to-do created by %s: %s", user_id, title)
        flash("Task is successfully created.", "success")
        return redirect(url_for('auth_dashboard.dashboard'))
    return render_template("/form.html")
