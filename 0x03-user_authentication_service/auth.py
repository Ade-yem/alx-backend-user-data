#!/usr/bin/env python3
"""Hash password"""

import uuid
from bcrypt import hashpw, gensalt, checkpw
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

    def valid_login(self, email: str, password: str) -> bool:
        """checks for login details"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create a session for the user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from session id"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """reset password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, hashed_password=_hash_password(password),
                             reset_token=None)


def _hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string"""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    return str(uuid.uuid4())
