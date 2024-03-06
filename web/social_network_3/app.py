#!/usr/bin/env python3

import re
import jwt
import random

from flask import Flask, render_template, render_template_string, request, make_response, redirect, url_for, g
from jinja2.exceptions import TemplateNotFound
from datetime import datetime, timedelta
from os import urandom

from database.database import Database
from usermodel import User

"""
App configuration
"""

app = Flask(__name__)
app.config.update(
    # Options
    # DEBUG=True,
    # Secrets
    TOKEN_ALGORITHM = 'HS256',
    SECRET_KEY = '8966a0ab5017bd3a0e3f0a44f14aa3c3ddfcff86c2404ef8ae9b1a65c752bdbd',
    ADMIN_OTP = ("%06d" % (int.from_bytes(urandom(3), byteorder='little') % 1000000)),
    # Names
    JWT = 'session_token',
    MFA = 'validation_otp',
    DESCRIPTIONS = "static/descriptions.txt"
)

"""
Database functions
"""

def get_db():
    conn = getattr(g, 'db', None)
    if conn is None:
        conn = g.database = Database("database/database.db")
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

"""
Decorators
"""

"""
Login required decorator
    - Pass required role as argument
    - Roles are "user", "moderator", "admin"
    - None can be used to retrieve optional username from token
"""
def login_required(required_role: str):
    def decorator(f):
        def wrapper(*args, **kwargs):
            current_user = None

            token = request.cookies.get(app.config['JWT'])
            if token:
                algorithm = app.config["TOKEN_ALGORITHM"]
                try:
                    # Fix previous algorithm confusion here
                    current_user = jwt.decode(
                        token, app.config['SECRET_KEY'], algorithms=[algorithm]
                    )
                except:
                    pass
            
            # A role is required but token is invalid or inexistant
            if required_role and current_user is None:
                return redirect(url_for('login', error="Login required !"))

            # User is logged but his role is insufficient
            if current_user and not (User.allow(current_user["role"], required_role)):
                return redirect(url_for('login', error=f"Insufficient privilegies ! ({required_role} required)"))

            return f(current_user, *args, **kwargs)

        # Fix multiples wrapper definitions :
        # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        wrapper.__name__ = f.__name__
        return wrapper

    return decorator

"""
Render helper
"""

def user_description(user):
    user_desc = None
    desc = get_db().get_description(user) if user else None

    if desc:
        user_desc = render_template_string(
            "%s's description: %s" % (user.capitalize(), desc)
        )

    return user_desc


def render(template, user=None, error=None, info=None, **kwargs):
    username = user.get("username") if user else None
    return render_template(
        template,
        user=username, description=user_description(username), error=error, info=info, **kwargs
    )

"""
App routes
"""

@app.route('/')
@login_required(None)
def home(current_user):
    posts = get_db().get_posts(limit=5, status=Database.POST_ACCEPTED) if current_user else None
    return render("index.html", user=current_user, posts=posts)


@app.route('/login', methods=["GET", "POST"])
@login_required(None)
def login(current_user):
    error_msg, info_msg = None, None

    # GET: Return login page
    if request.method == "GET":
        error_msg = request.args.get('error')
        info_msg = request.args.get('info')

    # POST: User attempt to login
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if not (username and password):
            error_msg = "Missing username and/or password"
        else:
            # Check for creds in database
            res = get_db().check_login(username, password)
            if res is not None:
                (user, role, mfa_enabled) = res
                now = datetime.utcnow()
                token = jwt.encode({
                    "username": user,
                    "role": role,
                    "iat": now,
                    "exp": now + timedelta(hours=1)
                }, app.config['SECRET_KEY'], algorithm=app.config['TOKEN_ALGORITHM'])

                # Redirection after login
                path = url_for('mfa') if mfa_enabled else url_for('home')
                # Set JWT as a cookie upon valid authentication
                resp = make_response(redirect(path))
                resp.set_cookie(app.config['JWT'], token)
                return resp

            else:
                error_msg = "Invalid username and/or password"

    # Return login page with user and error message
    return render("login.html", user=current_user, error=error_msg, info=info_msg)


@app.route('/mfa/validate', methods=['GET', 'POST'])
@login_required(User.USER)
def mfa(current_user):
    error_msg = None

    if request.method == "POST":
        otp = request.form.get("otp")

        if otp:
            if otp == str(app.config['ADMIN_OTP']):
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie(app.config['MFA'], otp)
                return resp
            else:
                error_msg = "Invalid validation code !"
        else:
            error_msg = "Missing validation code !"

    return render("validation.html", user=current_user, error=error_msg)


@app.route('/register', methods=['GET', 'POST'])
@login_required(None)
def register(current_user):
    error_msg = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not (username and password):
            error_msg = "Missing username and/or password"
        elif not re.match('^[a-zA-Z0-9_-]+$', username):
            error_msg = "Username can only contains letters, digits, '_' and '-' caracters"
        else:
            if get_db().user_exists(username):
                error_msg = "User already exists"
            else:
                get_db().create_user(username, password, role=User.ADMIN)
                return redirect(url_for('login', user=current_user, info="Successfully registered !"))

    return render("register.html", user=current_user, error=error_msg)
   

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie(app.config['JWT'], expires=0)
    resp.set_cookie(app.config['ADMIN_OTP'], expires=0)
    return resp

"""
Profile pages accessible after log in
"""

# Randomly generate n description
def generate_description(n: int):
    with open(app.config['DESCRIPTIONS'], 'r') as fdesc:
        user_descriptions = fdesc.read().split('\n')[:-1]

    return random.sample(user_descriptions, n)

@app.route('/profile', methods=['GET', 'POST'])
@login_required(User.USER)
def profile(current_user):
    error_msg, info_msg = None, None

    if request.method == "POST":
        description = request.form.get("desc")
        if not description:
            error_msg = "Empty description received"
        else:
            get_db().set_description(
                current_user.get("username"),
                description
            )
            info_msg = "Successfully update description"

    return render(
        "logged/profile.html",
        user=current_user, role=current_user.get("role"), error=error_msg, info=info_msg,
        options=generate_description(5)
    )


@app.route('/friends')
@login_required(User.USER)
def friends(current_user):
    return render("logged/friends.html", user=current_user)


@app.route('/newpost', methods=["GET", "POST"])
@login_required(User.USER)
def create_post(current_user):
    info_msg = None
    error_msg = None

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = current_user.get("username")
        if title and content and author:
            success = get_db().new_post(title, content, author)
            if not success:
                error_msg = "An error occured during post creation"
            else:
                info_msg = "Successfully created post !"
        else:
            error_msg = "Missing title and/or content"

    return render("logged/createpost.html", user=current_user, error=error_msg, info=info_msg)


@app.route('/settings', methods=["GET", "POST"])
@login_required(User.USER)
def settings(current_user):
    error_msg = None
    if request.method == "POST" and request.form.get("newpassword"):
        error_msg = "Password reset feature coming soon !"
    return render("logged/settings.html", user=current_user, error=error_msg)


@app.route('/search', methods=["GET", "POST"])
@login_required(User.USER)
def search(current_user):
    # POST with user and token parameter
    user = request.form.get("user")

    if request.method == "POST" and user:
        results = get_db().search_users(user)
        return render("logged/search.html", user=current_user, users=results, search=True)

    # Other requests
    return render("logged/search.html", user=current_user)

"""
Accessible to moderator and administrator
"""

@app.route('/moderation', methods=['GET', 'POST'])
@login_required(User.MODERATOR)
def moderation(current_user):
    error_msg = None
    info_msg = None
    pending_posts = get_db().get_posts(status=Database.POST_PENDING)
    refused_posts = get_db().get_posts(status=Database.POST_REFUSED, comment=True)

    if request.method == "POST":
        post_id = int(request.form.get("post_id"))
        status  = request.form.get("status")
        comment = request.form.get("comment")

        # Check status value
        if status not in [Database.POST_ACCEPTED, Database.POST_REFUSED]:
            error_msg = "Invalid post status"
        # Ensure that the selected post is in pending or refused status
        elif post_id not in [p[0] for p in pending_posts]:
            error_msg = "This post status isn't pending"
        # All good, update post status
        else:
            get_db().update_post(post_id, status, comment=comment)
            # Update posts lists
            pending_posts = get_db().get_posts(status=Database.POST_PENDING)
            refused_posts = get_db().get_posts(status=Database.POST_REFUSED, comment=True)
            info_msg = "Successfully update post !"
    
    return render(
        "logged/moderation.html",
        user=current_user, pending=pending_posts, refused=refused_posts,
        error=error_msg, info=info_msg
    )

"""
Administrator only
"""

# Administration panel
@app.route('/admin', methods=['GET', 'POST'])
@login_required(User.ADMIN)
def administration(current_user):
    error_msg = None
    info_msg = None
    posts = get_db().get_posts(status=Database.POST_REFUSED, comment=True)

    if request.method == "POST":
        post_id = int(request.form.get("post_id"))
        status  = request.form.get("status")

        # Check status value
        if status not in [Database.POST_ARCHIVED, Database.POST_DELETED]:
            error_msg = "Invalid post status"
        # Ensure that the selected post is in refused status
        elif post_id not in [p[0] for p in posts]:
            error_msg = "This post status isn't refused"
        # All good, update post status
        else:
            get_db().update_post(post_id, status)
            # Update refused posts list
            posts = get_db().get_posts(status=Database.POST_REFUSED, comment=True)
            info_msg = "Successfully update post !"
    
    return render(
        "logged/admin.html",
        user=current_user, refused=posts, error=error_msg, info=info_msg
    )


# Run the app
if __name__ == "__main__":
    with app.app_context():
        # app.logger.debug("Initialize database")
        # get_db().create_tables()
        app.logger.debug("Start server")
        app.logger.debug(f"Admin validation code: {app.config['ADMIN_OTP']}")
        app.run()
