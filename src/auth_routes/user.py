from flask import Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, logout_user
from src.config import app_log
import userManagement as dbHandler

auth_user_bp = Blueprint('auth_user', __name__)

@auth_user_bp.route('/delete_account', methods=['POST'])
@login_required
def deleteUser():
    '''
    Removes current user from database
    '''
    user_id = current_user.id
    try:
        dbHandler.deleteUserById(user_id)
        logout_user()
        app_log.info("Successful account deletion: %s", user_id)
        return redirect(url_for('index'))
    except Exception as e:
        app_log.error("Failed account deletion attempt %s: %s", user_id, str(e))
        flash("An error occurred while trying to delete your account. Please try again.", "error")
    return redirect(url_for('dashboard'))

@auth_user_bp.route('/download_data', methods=['GET'])
@login_required
def downloadUser():
    '''
    Download user data as JSON
    '''
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Incorrect User"}), 400
    user = dbHandler.getUserById(user_id)
    if current_user.id != user_id:
        app_log.info("Unauthorized access %s: %s", current_user, user_id)
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "user_id": user.id,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
    }

    response = jsonify(user_data)
    response.headers["Content-Disposition"] = f"attachment;filename=user_data_{user_id}.json"
    return response
