#!/usr/bin/env python3
"""
new Flask view that handles all routes
for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route("/auth_session/login", strict_slashes=False, methods=["POST"])
def auth_session():
    """handle session login"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user_instance = User()
    user_instance.email = email
    user_instance.password = password
    # user_instance.save()

    # all_users = User.search({"email": email})
    if not User.search({"email": email}):
        return jsonify({"error": "no user found for this email"}), 404

    is_valid_password = User.is_valid_password(user_instance, password)
    if not is_valid_password:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    user_session_id = auth.create_session(user_instance.id)

    session_name = os.getenv("SESSION_NAME")

    user_json = jsonify(user_instance.to_json())
    user_json.set_cookie(session_name, user_session_id)

    return user_json


@app_views.route("/auth_session/logout", strict_slashes=False, methods=["DELETE"])
def user_logout():
    """logs user out"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
