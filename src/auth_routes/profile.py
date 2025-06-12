from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
import userManagement as dbHandler

auth_profile_bp = Blueprint('profile', __name__)

@auth_profile_bp.route("/profile.html", methods=["GET", "POST"])
@login_required
def profile():
    completed, ongoing, overdue = dbHandler.recordStatus(current_user.id)
    name = dbHandler.getUserById(current_user.id)
    return render_template("profile.html", completed=completed, ongoing=ongoing, overdue=overdue)

@auth_profile_bp.route("/delete_todo/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id):
    dbHandler.deleteTodo(current_user.id, todo_id)
    return redirect(url_for("dashboard.dashboard"))

@auth_profile_bp.route("/complete_todo/<int:todo_id>", methods=["POST"])
@login_required
def complete_todo(todo_id):
    dbHandler.statusTodo(current_user.id, todo_id)
    return redirect(url_for("dashboard.dashboard"))

@auth_profile_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    '''
    Logout for logged in
    '''
    logout_user()
    flash("You have been logged out.", "info")
    return redirect('/index.html')
