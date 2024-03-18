#!/usr/bin/env python3
"""Handle views al routes for Session Authentication
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
        strict_slashes=False)   # noqa: E502, E128
def login() -> str:
    """POST /api/v1/auth_session/login
    Create a session for a user
    Parameters:
        - email: str
        - password: str
    Return:
        -
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    matches = User.search(attributes={"email": email})
    if not matches or len(matches) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = matches[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session for this user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
        strict_slashes=False)   # noqa: E502, E128
def logout() -> str:
    """DELETE /api/v1/auth_session/logout
    Logout a specied user based on session
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
