#!/usr/bin/env python3
"""Basic auth"""

from typing import TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns None - authorization_header"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns None - base64_authorization_header"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            import base64
            base64_authorization_header = base64.b64decode(
                base64_authorization_header)
            return base64_authorization_header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns None - decoded_base64_authorization_header"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """returns None - user_email, user_pwd"""
        if user_email is None or user_pwd is None or not isinstance(
                user_email, str) or not isinstance(user_pwd, str):
            return None
        from models.user import User
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads the Auth and retrieves the User instance for a request"""
        req = self.authorization_header(request)
        if req is None:
            return None
        req = self.extract_base64_authorization_header(req)
        req = self.decode_base64_authorization_header(req)
        user = self.extract_user_credentials(req)
        user = self.user_object_from_credentials(user[0], user[1])
        return user
