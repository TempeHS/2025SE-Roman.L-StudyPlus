import sqlite3 as sql
import time
import random
from datetime import datetime, timedelta
from flask import flash, redirect, url_for, g
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
    def __init__(self, user_id, email, firstname, lastname):
        self.id = user_id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

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
    cur.execute("SELECT id, email, password, firstname, lastname FROM users WHERE email = ?", (email,))
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
        return User(user[0], user[1], user[3], user[4])
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
    cur.execute("SELECT id, title, due_date, label, body, status FROM todos WHERE user_id = ? ORDER BY date DESC", (user_id,))
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

def statusTodo(user_id, todo_id):
    db = get_db()
    cur = db.cursor()
    # Get current status
    cur.execute("SELECT status FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
    row = cur.fetchone()
    if row is not None:
        status = row[0]
        # Toggle: if already complete (1), set to 0; else set to 1
        new_status = 0 if status == 1 else 1
        cur.execute("UPDATE todos SET status = ? WHERE id = ? AND user_id = ?", (new_status, todo_id, user_id))
        db.commit()

def deleteTodo(user_id, todo_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
    db.commit()

def recordStatus(user_id):
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
