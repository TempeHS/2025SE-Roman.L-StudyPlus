from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from src import sanitize_and_validate as sv
import userManagement as dbHandler

auth_dashboard_bp = Blueprint('auth_dashboard', __name__)

def days_left(todos):
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
    return todos

@auth_dashboard_bp.route("/dashboard.html", methods=["GET", "POST"])
@login_required
def dashboard():
    todos = dbHandler.getTodos(current_user.id)
    todos = days_left(todos)
    return render_template("dashboard.html", todos=todos, now=datetime.now())

@auth_dashboard_bp.route('/search', methods=["GET", "POST"])
@login_required
def search_todos():
    '''
    Search to-dos for the logged-in user
    '''
    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'all')
    safe_query = sv.sanitizeQuery(query)

    # if filter_type == 'label':
        # todos = dbHandler.searchTodosByLabel(current_user.id, safe_query)
    if filter_type == 'date':
        todos = dbHandler.searchTodosByDate(current_user.id, safe_query)
    elif filter_type == 'content':
        todos = dbHandler.searchTodosByContent(current_user.id, safe_query)
    else:
        todos = dbHandler.searchTodosAll(current_user.id, safe_query)
    todos = days_left(todos)
    return render_template('dashboard.html', todos=todos)
