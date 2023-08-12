#!/usr/bin/env python3
"""Session expiration"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration"""

    def __init__(self):
        """Constructor"""
        sess_dur = int(getenv('SESSION_DURATION'))
        if not sess_dur:
            self.session_duration = 0
        else:
            self.session_duration = sess_dur

    def create_session(self, user_id=None):
        """create session with user id"""
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        session_dictionary = {
            'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """overloads the super function"""
        if session_id is not None:
            return None
        sess = self.user_id_by_session_id[session_id]
        if not sess:
            return None
        if self.session_duration <= 0:
            return sess.get('user_id')
        if 'created_at' not in sess:
            return None
        created_at = sess.get('created_at')
        ti = created_at + timedelta(seconds=self.session_duration)
        if ti < datetime.now():
            return None
        return sess.get('user_id')
