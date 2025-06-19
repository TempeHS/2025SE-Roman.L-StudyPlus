from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
import userManagement as dbHandler

auth_dashboard_bp = Blueprint('auth_dashboard', __name__)

@auth_dashboard_bp.route("/dashboard.html", methods=["GET", "POST"])
@login_required
def dashboard():
    todos = dbHandler.getTodos(current_user.id)
    for todo in todos:
        due = todo.get('due_date')
        if due:
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
    return render_template("dashboard.html", todos=todos, now=datetime.now())
