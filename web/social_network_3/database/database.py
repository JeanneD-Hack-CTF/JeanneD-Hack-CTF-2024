#!/usr/bin/env python3

import sqlite3

# Interactions with DB, creation, request, insert...

class Database():
    
    # Constants
    INIT_SCRIPT = "database/schema.sql"

    POST_PENDING = "pending"
    POST_ACCEPTED = "accepted"
    POST_REFUSED = "refused"
    POST_ARCHIVED = "archived"
    POST_DELETED = "deleted"

    POST_ALL_STATUS = [
        POST_PENDING, POST_ACCEPTED, POST_REFUSED,
        POST_ARCHIVED, POST_DELETED
    ]

    REL_PENDING = "pending"
    REL_ACCEPTED = "accepted"
    REL_REFUSED = "refused"

    """
    Creation, open and close functions
    """

    # Constructor
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(self.name)

    # Database creation
    def create_tables(self):
        with open(self.INIT_SCRIPT, 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()
    
    # Close database
    def close(self):
        self.conn.close()

    """
    Login
    """

    # Check user credentials in database
    def check_login(self, user: str, password: str):
        cursor = self.conn.cursor()
        query = """
            SELECT username, role, mfa_enabled
            FROM users
            WHERE username = ? AND password = ?
        """
        # Fetch only first result because user are uniques
        r = cursor.execute(query, (user, password)).fetchone()
        cursor.close()
        return r

    """
    User relative functions
    """

    # Research users in database
    def search_users(self, user: str):
        cursor = self.conn.cursor()
        # Previous SQLi fixed
        query = """
            SELECT username, role, created
            FROM users
            WHERE username LIKE ?
        """
        r = cursor.execute(query, (user+'%',)).fetchall()
        cursor.close()
        return r

    # Check if user exists in database
    def user_exists(self, user: str) -> bool:
        cursor = self.conn.cursor()
        query = """
            SELECT id, username
            FROM users
            WHERE username = ?
        """
        r = cursor.execute(query, (user,)).fetchall()
        cursor.close()
        return len(r) > 0

    # Create a new user in the database (by default with role 'user')
    def create_user(self, user: str, passwd: str, role="user"):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (user, passwd, role))
        id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return id

    # Return user id from username
    def get_user_id(self, username: str) -> int:
        cursor = self.conn.cursor()
        query = """
            SELECT id
            FROM users
            WHERE username = ?
        """
        r = cursor.execute(query, (username,)).fetchone()
        cursor.close()
        return r[0] if r else None

    # Return username from user id
    def get_username(self, id: int) -> str:
        cursor = self.conn.cursor()
        query = """
            SELECT username
            FROM users
            WHERE id = ?
        """
        r = cursor.execute(query, (id,)).fetchone()
        cursor.close()
        return r[0] if r else None

    def get_description(self, username: str):
        cursor = self.conn.cursor()
        query = """
            SELECT description
            FROM users
            WHERE username = ?
        """
        r = cursor.execute(query, (username,)).fetchone()
        cursor.close()
        return r[0] if r else None

    def set_description(self, username: str, desc: str):
        cursor = self.conn.cursor()
        query = """
            UPDATE users
            SET description = ?
            WHERE username = ?
        """
        r = cursor.execute(query, (desc, username))
        cursor.close()
        self.conn.commit()

    """
    Posts relative functions
    """

    # Create a new post, return True if the insert success else Flase
    def new_post(self, title: str, content: str, author: str) -> bool:
        author_id = self.get_user_id(author)
        if author_id:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO posts (title, content, author, status)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (title, content, author_id, self.POST_PENDING))
            cursor.close()
            self.conn.commit()
        return author_id is not None

    # Return the last :limit posts, filtered by status (all by default)
    def get_posts(self, limit: int=None, status: str=None, comment=False):
        cursor = self.conn.cursor()
        query = "SELECT id, author, title, content FROM posts"
        if comment:
            query = "SELECT id, author, title, content, comment FROM posts"
        # Add status if defined
        if status: 
            query += " WHERE status = ?"
        # Order posts
        query += " ORDER BY created DESC"

        if status:
            r = cursor.execute(query, (status,)).fetchall()
        else:
            r = cursor.execute(query).fetchall()
        cursor.close()

        # Cut posts
        if limit:
            r = r[:limit]

        # Resolve author's username from id
        posts = []
        for p in r:
            if comment:
                id, author_id, title, content, comm = p
                posts.append((id, self.get_username(author_id) or "Unknown", title, content, comm))
            else:
                id, author_id, title, content = p
                posts.append((id, self.get_username(author_id) or "Unknown", title, content))
        return posts
    
    # Update a post status
    def update_post(self, post_id: int, status: str, comment: str=None):
        cursor = self.conn.cursor()
        # Update status
        query = """
            UPDATE posts
            SET status = ?
            WHERE id = ?
        """
        cursor.execute(query, (status, post_id))
        # Update comment if exists
        if comment:
            query = """
                UPDATE posts
                SET comment = ?
                WHERE id = ?
            """
            cursor.execute(query, (comment, post_id))
        # Apply changes
        cursor.close()
        self.conn.commit()
    
    """
    Friends relative functions
    """

    # Send a friends request
    def send_friends_request(asker: str, receiver: str):
        asker_id = self.get_user_id(asker)
        receiver_id = self.get_user_id(receiver)

        if asked_id and receiver_id:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO relations (user_asking, user_receiving, relationship)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (asked_id, receiver_id, REL_PENDING))
            cursor.close()
            self.conn.commit()
            return True

        return False

    # Accept or refuse a friends request
    def update_friends_request(request_id: int, accepted: bool):
        cursor = self.conn.cursor()
        query = """
            UPDATE relations
            SET relationship = ?
            WHERE id = ?
        """
        status = REL_ACCEPTED if accepted else REL_REFUSED
        cursor.execute(query, (status, request_id))
        cursor.close()
        self.conn.commit()
