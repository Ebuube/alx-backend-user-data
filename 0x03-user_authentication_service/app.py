#!/usr/bin/env python3
"""Minimal Flask app
"""
from auth import Auth
from flask import (Flask, jsonify, request, abort, make_response,
                   url_for, redirect)


AUTH = Auth()
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/", methods=["GET"])
def home():
    """Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_users():
    """Register a new user
    Parameters in Form data:
        * email: str
        * password: str
    """
    required = ['email', 'password']
    for attr in required:
        if attr not in request.form:
            return jsonify({"Error": f"{attr} missing"}), 400
    try:
        user = AUTH.register_user(
                request.form.get('email'),
                request.form.get('password'))
    except ValueError as e:
        print(e)
        return jsonify({"message": "email already registered"}), 400
    return jsonify({
        "email": user.email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Create a session for user
    Parameters in Form data:
        * email: str
        * password: str
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", AUTH.create_session(email))
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """End current session of this user
    session_id cookie is expected
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user_id=user.id)
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetch user profile by session_id
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Generate a reset password token and return it
    Form-data parameters:
        * email: str
    """
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
