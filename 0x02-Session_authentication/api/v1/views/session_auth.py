#!/usr/bin/env python3
"""routes for the Session authentication"""

import os
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login() -> str:
    """login route"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not pwd or pwd == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 400
    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            sess_name = os.getenv('SESSION_NAME')
            res.set_cookie(sess_name, sess_id)
            return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """logout route"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
