#!/usr/bin/python3

import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for
from jinja2.exceptions import TemplateNotFound
from functools import wraps
from os import urandom

"""
Y: a new social network
"""

# App configuration

app = Flask(__name__)
app.config.update(
    # DEBUG=True,
    SECRET_KEY='63d562b658170d405c53473ed676d7ab791604f8f469e42d9860b742a8525e1e'
)

# Decorators

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("user"):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error="Login required !"))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("role") == "administrator":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error="You are not admin !"))
    return wrap

# Interactions with DB

DB_NAME = "database.db"

# Helpers

def db_connect():
    connection = sqlite3.connect(DB_NAME)
    return connection

# Check user credentials in database
# Avoid SQLi here
def db_check_login(user: str, password: str):
    conn = db_connect()
    cursor = conn.cursor()
    query = """
        SELECT username, role
        FROM users
        WHERE username = ? AND password = ?
    """
    r = cursor.execute(query, (user, password)).fetchone()    # User are uniques
    conn.close()
    return r

# Research users in database
# SQLi is here
def db_search_users(user: str):
    conn = db_connect()
    cursor = conn.cursor()
    query = f"""
        SELECT username, created
        FROM users
        WHERE username LIKE '{user}%'
    """
    r = cursor.execute(query).fetchall()
    conn.close()
    return r

# Database creation
INIT_SCRIPT = "schema.sql"

def create_db():
    connection = db_connect()
    with open(INIT_SCRIPT) as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

# Routes

@app.route('/')
def home():
    return render_template("index.html")

# Creds leak here
@app.route('/login', methods=["GET", "POST"])
def login():
    error_msg = None
    # GET: Return login page
    if request.method == "GET":
        error_msg = request.args.get('error')
    # POST: User attempt to login
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if not (username and password):
            error_msg = "Missing username and/or password"
        else:
            # Temp. check for creds
            res = db_check_login(username, password)
            if res is not None:
                (user, role) = res
                session["user"] = user
                session["role"] = role
            else:
                error_msg = "Login failed"
    # Return login page with user and error message
    return render_template("login.html", user=session.get("user"), error=error_msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Profile, LFI here
@app.route('/profile')
@login_required
def profile():
    error_msg = None
    page = request.args.get("p")
    if page:
        try:
            resp = render_template(f"pages/{page}.html")
            return resp
        except TemplateNotFound:
            error_msg = "Page not found"
    return render_template("profile.html", error=error_msg)

@app.route('/resetpassword', methods=["POST"])
@login_required
def resetpwd():
    return render_template("pages/settings.html", resetpassword=True)

# SQLi here
@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    # POST with user and token parameter
    user = request.form.get("user")
    token = request.form.get("token")   # Token to force the intended way
    if request.method == "POST" and user and token:
        results = db_search_users(user)
        # app.logger.debug(f"User search results: {results}")
        return render_template("pages/search.html", users=results, search=True)
    # Other requests
    else:
        return "This feature is under construction", 404

# Flag is here
@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template("admin.html")


# Run the app
if __name__ == "__main__":
    print("[+] Initialize database")
    create_db()
    print("[+] Start server")
    app.run()
