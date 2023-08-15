#!/usr/bin/env python3
"""Hash password"""

from bcrypt import hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

def _hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string"""
    return hashpw(password.encode('utf-8'), gensalt())
