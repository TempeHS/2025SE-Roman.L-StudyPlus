from flask import Blueprint, render_template, request, redirect, url_for, flash
from src import sanitize_and_validate as sv, password_hashing as psh
import userManagement as dbHandler

auth_signup_bp = Blueprint('auth', __name__)

@auth_signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    '''
    Create an account
    '''
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        if dbHandler.userExists(email):
            flash('User already exists!', 'error')
            return redirect(url_for('auth.signup'))
        if not sv.validatePassword(password):
            flash('Invalid password format!', 'error')
            return redirect(url_for('auth.signup'))
        if not sv.validateEmail(email):
            flash('Invalid email format!', 'error')
            return redirect(url_for('auth.signup'))
        if not sv.validateName(firstname, lastname):
            flash('No numbers for first and last name!', 'error')
            return redirect(url_for('auth.signup'))

        password = psh.hashPassword(password)
        firstname = firstname.capitalize()
        lastname = lastname.capitalize()
        dbHandler.insertUser(email, password, firstname, lastname)
        return render_template("/index.html")
    return render_template("/signup.html")
