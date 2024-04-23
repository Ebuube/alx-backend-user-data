#!/usr/bin/env python3
"""Authentication
"""
import bcrypt


def _hash_password(password: str = '') -> bytes:
    """Return a salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd
