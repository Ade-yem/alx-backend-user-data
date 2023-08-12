#!/usr/bin/env python3
"""session model"""

from models.base import Base


class UserSession(Base):
    """User session model"""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
