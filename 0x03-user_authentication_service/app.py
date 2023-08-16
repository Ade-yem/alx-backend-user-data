#!/usr/bin/env python3
"""Basic flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
      - JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """register user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """handle login sessions"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """handle logout"""
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if not user or not session_id:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """handle profile request"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user or not session_id:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password ', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """reset password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
