#!/usr/bin/env python3
"""End-to-end integration test
"""
import requests

_base_url = "http://localhost:5000/"


def register_user(email: str, password: str) -> None:
    """Test registering a user
    """
    url = _base_url + "users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password
    """
    url = _base_url + "users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 400


def log_in(email: str, password: str) -> str:
    """Test login with correct password
    """
    url = _base_url + "sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Try fetching profile prior to login
    """
    url = _base_url + "profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Try fetching profile after login
    """
    url = _base_url + "profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Test logging out
    """
    url = _base_url + "sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Test getting reset password token
    """
    url = _base_url + "reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    rj = response.json()
    return rj.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating user password
    """
    url = _base_url + "reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    '''
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
    '''
