#!/usr/bin/env python3
"""authentication database"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import logging

logging.basicConfig(filename='app.py', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class SessionDBAuth(SessionExpAuth):
    """Authentication database class"""

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        sess_id = super().create_session(user_id)
        if isinstance(sess_id, str):
            kwargs = {
                'user_id': user_id, 'session_id': sess_id
            }            
            user_sess = UserSession(**kwargs)
            user_sess.save()
            return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ returns the User ID by requesting UserSession in the
         database based on session_id"""
        try:
            user_sess = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if not user_sess or user_sess == []:
            return None
        ti = user_sess[0].created_at + timedelta(seconds=self.session_duration)
        if ti < datetime.now():
            return None
        return user_sess[0].user_id

    def destroy_session(self, request=None):
        """that destroys the UserSession based on the Session ID
         from the request cookie"""
        if not request:
            return None
        sess_id = self.session_cookie(request)
        user_sess = UserSession.search({'session_id': sess_id})
        if not user_sess or user_sess == []:
            return False
        del user_sess[0]
        return True
