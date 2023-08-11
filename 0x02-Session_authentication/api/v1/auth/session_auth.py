#!/usr/bin/env python3
"""Session auth"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        self.id = str(uuid.uuid4())
        self.user_id_by_session_id[self.id] = user_id
        return self.id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """that returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """(overload) that returns a User instance based on a cookie value"""
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        from models.user import User
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """that deletes the user session / logout"""
        if not request:
            return None
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id
        if not user_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
