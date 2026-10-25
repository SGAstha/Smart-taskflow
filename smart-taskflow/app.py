import os
import sqlite3
from datetime import datetime, date
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "taskflow.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                category TEXT NOT NULL DEFAULT 'General',
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)


init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    if "user_id" not in session:
        return None
    with get_db() as conn:
        return conn.execute("SELECT id, name, email FROM users WHERE id = ?", (session["user_id"],)).fetchone()


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("Please complete every field.", "error")
            return render_template("register.html")
        if len(password) < 8:
            flash("Use a password with at least 8 characters.", "error")
            return render_template("register.html")
        try:
            with get_db() as conn:
                cur = conn.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password))
                )
                session["user_id"] = cur.lastrowid
                session["user_name"] = name
            flash("Your account is ready. Let's plan your day!", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("An account with that email already exists.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "All")
    category_filter = request.args.get("category", "All")
    query = "SELECT * FROM tasks WHERE user_id = ?"
    params = [session["user_id"]]
    if q:
        query += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        params.extend([f"%{q}%"] * 3)
    if status_filter in ("Pending", "In Progress", "Completed"):
        query += " AND status = ?"
        params.append(status_filter)
    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    query += """ ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
                 CASE WHEN due_date = '' THEN 1 ELSE 0 END, due_date ASC, created_at DESC"""
    with get_db() as conn:
        tasks = conn.execute(query, params).fetchall()
        all_tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (session["user_id"],)).fetchall()
    today = date.today().isoformat()
    total = len(all_tasks)
    completed = sum(t["status"] == "Completed" for t in all_tasks)
    pending = sum(t["status"] == "Pending" for t in all_tasks)
    in_progress = sum(t["status"] == "In Progress" for t in all_tasks)
    overdue = sum(bool(t["due_date"]) and t["due_date"] < today and t["status"] != "Completed" for t in all_tasks)
    categories = sorted({t["category"] for t in all_tasks})
    chart_data = {
        "statusLabels": ["Pending", "In Progress", "Completed"],
        "statusValues": [pending, in_progress, completed],
        "categoryLabels": categories or ["No tasks yet"],
        "categoryValues": [sum(t["category"] == c for t in all_tasks) for c in categories] or [0]
    }
    return render_template(
        "dashboard.html", user=user, tasks=tasks, total=total, completed=completed,
        pending=pending, in_progress=in_progress, overdue=overdue, chart_data=chart_data,
        q=q, status_filter=status_filter, category_filter=category_filter, categories=categories, today=today
    )


@app.route("/tasks/new", methods=["POST"])
@login_required
def create_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("A task title is required.", "error")
        return redirect(url_for("dashboard"))
    category = request.form.get("category", "General").strip() or "General"
    priority = request.form.get("priority", "Medium")
    if priority not in ("Low", "Medium", "High"):
        priority = "Medium"
    due_date = request.form.get("due_date", "")
    status = request.form.get("status", "Pending")
    if status not in ("Pending", "In Progress", "Completed"):
        status = "Pending"
    with get_db() as conn:
        conn.execute("""
            INSERT INTO tasks (user_id, title, description, category, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], title, request.form.get("description", "").strip(),
              category, priority, due_date, status))
    flash("Task added successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/tasks/<int:task_id>/update", methods=["POST"])
@login_required
def update_task(task_id):
    status = request.form.get("status", "")
    if status not in ("Pending", "In Progress", "Completed"):
        flash("Choose a valid task status.", "error")
        return redirect(url_for("dashboard"))
    with get_db() as conn:
        cur = conn.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
                           (status, task_id, session["user_id"]))
    flash("Task status updated." if cur.rowcount else "Task not found.", "success" if cur.rowcount else "error")
    return redirect(url_for("dashboard"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    flash("Task deleted." if cur.rowcount else "Task not found.", "success" if cur.rowcount else "error")
    return redirect(url_for("dashboard"))


@app.route("/tasks/<int:task_id>/edit", methods=["POST"])
@login_required
def edit_task(task_id):
    title = request.form.get("title", "").strip()
    if not title:
        flash("A task title is required.", "error")
        return redirect(url_for("dashboard"))
    priority = request.form.get("priority", "Medium")
    if priority not in ("Low", "Medium", "High"):
        priority = "Medium"
    status = request.form.get("status", "Pending")
    if status not in ("Pending", "In Progress", "Completed"):
        status = "Pending"
    with get_db() as conn:
        cur = conn.execute("""
            UPDATE tasks SET title=?, description=?, category=?, priority=?, due_date=?, status=?
            WHERE id=? AND user_id=?
        """, (title, request.form.get("description", "").strip(),
              request.form.get("category", "General").strip() or "General",
              priority, request.form.get("due_date", ""), status, task_id, session["user_id"]))
    flash("Task updated." if cur.rowcount else "Task not found.", "success" if cur.rowcount else "error")
    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
