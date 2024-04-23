#!/usr/bin/env python3
"""Minimal Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request


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
    Parameters in JSON payload:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
