from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from src.config import app_log
import userManagement as dbHandler

auth_profile_bp = Blueprint('auth_profile', __name__)

# Profiles
@auth_profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    '''
    Load current user profile
    '''
    completed, ongoing, overdue = dbHandler.recordStatus(current_user.id)
    labels, stats = dbHandler.get_progression_stats(current_user.id)
    return render_template("profile.html", user=current_user, completed=completed, ongoing=ongoing,
                            overdue=overdue, labels=labels, stats=stats)

@auth_profile_bp.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    '''
    Load public user profiles
    '''
    user = dbHandler.getUserById(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('auth_profile.preferences'))
    if user.privacy == 'private':
        flash("This profile is private.", "error")
        return redirect(url_for('auth_profile.preferences'))
    completed, ongoing, overdue = dbHandler.recordStatus(user_id)
    labels, stats = dbHandler.get_progression_stats(user_id)
    return render_template('profile.html', user=user, labels=labels, stats=stats,
                            completed=completed, ongoing=ongoing, overdue=overdue)

@auth_profile_bp.route('/profile/search', methods=['POST'])
@login_required
def profile_search():
    '''
    Search user profiles
    '''
    user_id = request.form.get('user_id', type=int)
    if user_id:
        return redirect(url_for('auth_profile.user_profile', user_id=user_id))

# To-do list
@auth_profile_bp.route("/delete_todo/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    '''
    Delete a to-do from the database
    '''
    try:
        dbHandler.deleteTodo(current_user.id, todo_id)
        flash("Task is successfully deleted.", "error")
        app_log.info("Successful todo deletion: user_id=%s, todo_id=%s", user_id, todo_id)
    except Exception as e:
        app_log.error("Failed todo deletion attempt user_id=%s, todo_id=%s: %s", 
        user_id, todo_id, str(e))
        flash("An error occurred while trying to delete your to-do. Please try again.", "error")
    return redirect(url_for("auth_dashboard.dashboard"))

@auth_profile_bp.route("/complete_todo/<int:todo_id>", methods=["POST"])
@login_required
def complete_todo(todo_id):
    '''
    Complete a to-do
    '''
    try:
        dbHandler.statusTodo(current_user.id, todo_id)
        flash("Task is successfully completed.", "success")
    except Exception as e:
        app_log.error("Failed todo completion attempt user_id=%s, todo_id=%s: %s", 
        current_user.id, todo_id, str(e))
        flash("An error occurred while trying to complete your to-do. Please try again.", "error")
    return redirect(url_for("auth_dashboard.dashboard"))

# Preferences
@auth_profile_bp.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    return render_template("preferences.html")

@auth_profile_bp.route('/set_layout', methods=['POST'])
@login_required
def set_layout():
    '''
    Set layout server-side
    '''
    layout = request.form.get('layout', 'sidebar')
    dbHandler.set_user_layout(current_user.id, layout)
    flash("Layout preference updated.", "success")
    return redirect(url_for('auth_profile.profile'))

@auth_profile_bp.route('/set_theme', methods=['POST'])
@login_required
def set_theme():
    '''
    Set privacy server-side
    '''
    privacy = request.form.get('privacy', 'public')
    dbHandler.set_user_privacy(current_user.id, privacy)
    flash("Privacy preference updated.", "success")
    return redirect(url_for('auth_profile.profile'))

@auth_profile_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    '''
    Logout for logged in
    '''
    logout_user()
    flash("You have been logged out.", "info")
    return redirect('/index.html')
