#!/usr/bin/env python3

"""
User model class
"""

class User():

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "administrator"

    ENUM_USERS = {
        "user": 1,
        "moderator": 2,
        "administrator": 3
    }

    def __init__(self, username, role):
        self.username = username
        self.role = role

    def is_admin():
        return self.role == ADMIN
    
    def is_moderator():
        return self.role == MODERATOR

    """
    Return True if asked_role is None or both roles are defined and user_role is
    greater than or equal to asked_role
    """
    @staticmethod
    def allow(user_role, asked_role):
        user_cst = User.ENUM_USERS.get(user_role)
        asked_cst = User.ENUM_USERS.get(asked_role)

        return (asked_role is None) or (user_cst and asked_cst and user_cst >= asked_cst)