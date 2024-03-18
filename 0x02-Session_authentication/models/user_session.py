#!/usr/bin/env python3
"""Persist Sessions in Database
"""
from models.base import Base


class UserSession(Base):
    """Storing User sessions in database
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initialization
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
