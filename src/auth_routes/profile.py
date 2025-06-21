from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from src.config import app_log

import userManagement as dbHandler

auth_profile_bp = Blueprint('auth_profile', __name__)

@auth_profile_bp.route("/profile.html", methods=["GET", "POST"])
@login_required
def profile():
    completed, ongoing, overdue = dbHandler.recordStatus(current_user.id)
    labels, stats = dbHandler.get_progression_stats(current_user.id)
    return render_template("profile.html", completed=completed, ongoing=ongoing, overdue=overdue, labels=labels, stats=stats)

@auth_profile_bp.route("/delete_todo/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    '''
    Delete a to-do from the database
    '''
    user_id = current_user.id
    try:
        dbHandler.deleteTodo(user_id, todo_id)
        app_log.info("Successful todo deletion: user_id=%s, todo_id=%s", user_id, todo_id)
    except Exception as e:
        app_log.error("Failed todo deletion attempt user_id=%s, todo_id=%s: %s", user_id, todo_id, str(e))
        flash("An error occurred while trying to delete your to-do. Please try again.", "error")
    return redirect(url_for("auth_dashboard.dashboard"))

#@auth_user_bp.route('/delete_log', methods=['POST'])
#@login_required
#def deleteLog():
    '''
    Delete log from database
    '''
    user_id = current_user.id
    log_id = request.form.get('log_id')
    try:
        dbHandler.deleteLogs(user_id, log_id)
        app_log.info("Successful log deletion: %s: %s", user_id, log_id)
    except Exception as e:
        app_log.error("Failed log deletion attempt %s: %s", user_id, str(e))
        flash("An error occurred while trying to delete your log. Please try again.", "error")
    return redirect(url_for('dashboard'))

@auth_profile_bp.route("/complete_todo/<int:todo_id>", methods=["POST"])
@login_required
def complete_todo(todo_id):
    dbHandler.statusTodo(current_user.id, todo_id)
    return redirect(url_for("auth_dashboard.dashboard"))

@auth_profile_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    '''
    Logout for logged in
    '''
    logout_user()
    flash("You have been logged out.", "info")
    return redirect('/index.html')
