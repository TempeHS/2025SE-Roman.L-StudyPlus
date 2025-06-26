import sqlite3 as sql
import time
import random
from datetime import datetime, timedelta
from flask import flash, g
from flask_login import UserMixin
from flask import Flask

app = Flask(__name__)

DATABASE = '.databaseFiles/database.db'

# Reusable connection
def get_db():
    if 'db' not in g:
        g.db = sql.connect(DATABASE)
        g.db.row_factory = sql.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

class User(UserMixin):
    '''
    User class for Flask-Login integration'''
    def __init__(self, user_id, email, firstname, lastname, layout, privacy):
        self.id = user_id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.layout = layout
        self.privacy = privacy

## User related functions
def insertUser(email, password, firstname, lastname):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO users (email, password, firstname, lastname, lastactivity) VALUES (?,?,?,?,?)", (email, password, firstname, lastname, datetime.now()))
    db.commit()
    return True

def userExists(email: str) -> bool:
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT email FROM users WHERE email = ?", (email,))
    exists = cur.fetchone() is not None
    db.commit()
    return exists

def retrieveUsers(email: str) -> tuple:
    time.sleep(random.uniform(0.1, 0.2))
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, email, password, firstname, lastname, layout, privacy FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    db.commit()
    return user if user else False

def getUserById(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    db.commit()
    if user:
        return User(user[0], user[1], user[3], user[4], user[9], user[10])
    return user

def deleteUserById(user_id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        flash("An error occurred while deleting the user.", "error")
        return False

def deleteUserByInactivity():
    db = get_db()
    cur = db.cursor()
    cutoff_date = datetime.now() - timedelta(days=180)
    cur.execute("DELETE FROM users WHERE last_activity < ?", (cutoff_date,))
    db.commit()

def updateLastActivity(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET lastactivity = ? WHERE id = ?", (datetime.now(), user_id))
    db.commit()

## To-Do List Functions
def addTodo(title, body, fullname, user_id, created_at, due_date, label):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO todos (title, body, fullname, user_id, created_at, due_date, label, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (title, body, fullname, user_id, created_at, due_date, label, 0)
    )
    db.commit()

def getTodos(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ?", (user_id,))
    todos = [
        {
            "id": row[0],
            "title": row[1],
            "due_date": row[2],
            "label": row[3],
            "body": row[4],
            "completed": row[5]
        }
        for row in cur.fetchall()
    ]    
    db.commit()
    return todos

def mapTodoRows(rows):
    ''' 
    Maps database rows to a list of dictionaries for todos.
    '''
    return [
        {
            "id": row[0],
            "title": row[1],
            "due_date": row[2],
            "label": row[3],
            "body": row[4],
            "completed": row[5]
        }
        for row in rows
    ]

def statusTodo(user_id, todo_id):
    """
    Toggle the status of a todo item between completed and ongoing.
    """
    db = get_db()
    cur = db.cursor()
    # Get current status
    cur.execute("SELECT status FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
    row = cur.fetchone()
    if row is not None:
        status = row[0]
        new_status = 0 if status == 1 else 1
        if new_status == 1:
            completed_at = datetime.now()
        else:
            completed_at = None
        cur.execute(
            "UPDATE todos SET status = ?, completed_at = ? WHERE id = ? AND user_id = ?",
            (new_status, completed_at, todo_id, user_id)
        )
        db.commit()

def deleteTodo(user_id, todo_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
    db.commit()

def recordStatus(user_id):
    """
    Returns the count of completed, ongoing, and overdue tasks for a user.
    """
    db = get_db()
    cur = db.cursor()
    # Completed
    cur.execute("SELECT COUNT(*) FROM todos WHERE user_id = ? AND status = 1", (user_id,))
    completed = cur.fetchone()[0]
    # Ongoing
    cur.execute("SELECT COUNT(*) FROM todos WHERE user_id = ? AND status = 0 AND due_date >= ?", (user_id, datetime.now()))
    ongoing = cur.fetchone()[0]
    # Overdue
    cur.execute("SELECT COUNT(*) FROM todos WHERE user_id = ? AND status = 0 AND due_date < ?", (user_id, datetime.now()))
    overdue = cur.fetchone()[0]

    cur.execute(
        "UPDATE users SET completed_task = ?, ongoing_task = ?, overdue_task = ? WHERE id = ?",
        (completed, ongoing, overdue, user_id)
    )
    db.commit()

    return completed, ongoing, overdue

## Search Function
def searchTodosByLabel(user_id, safe_query):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ? AND label LIKE ?", (user_id, f'%{safe_query}%'))
    data = cur.fetchall()
    db.commit()
    return mapTodoRows(data)

def searchTodosByDate(user_id, safe_query):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ? AND due_date LIKE ?", (user_id, f'%{safe_query}%'))
    data = cur.fetchall()
    db.commit()
    return mapTodoRows(data)

def searchTodosByContent(user_id, safe_query):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ? AND (title LIKE ? OR body LIKE ?)", (user_id, f'%{safe_query}%', f'%{safe_query}%'))
    data = cur.fetchall()
    db.commit()
    return mapTodoRows(data)

def searchTodosAll(user_id, safe_query):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ? AND (title LIKE ? OR body LIKE ? OR label LIKE ? OR due_date LIKE ?)",
        (user_id, f'%{safe_query}%', f'%{safe_query}%', f'%{safe_query}%', f'%{safe_query}%')
    )
    data = cur.fetchall()
    db.commit()
    return mapTodoRows(data)

def countTodosByUser(user_id):
    """
    Returns the total number of todos for a given user.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM todos WHERE user_id = ?", (user_id,))
    count = cur.fetchone()[0]
    db.commit()
    return count

## Profile
def get_progression_stats(user_id):
    """
    Returns the last 7 days of completed todos for a user.
    """
    db = get_db()
    cur = db.cursor()
    today = datetime.now().date()
    stats = []
    labels = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        cur.execute(
            "SELECT COUNT(*) FROM todos WHERE user_id = ? AND status = 1 AND DATE(completed_at) = ?",
            (user_id, day)
        )
        count = cur.fetchone()[0]
        stats.append(count)
        labels.append(day.strftime("%b %d"))
    return labels, stats

def set_user_layout(user_id, layout):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET layout = ? WHERE id = ?", (layout, user_id))
    db.commit()

def set_user_privacy(user_id, privacy):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET privacy = ? WHERE id = ?", (privacy, user_id))
    db.commit()
