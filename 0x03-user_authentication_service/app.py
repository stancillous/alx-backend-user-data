#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
app = Flask(__name__)

AUTH = Auth()


@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    """serve home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """end point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user_created = AUTH.register_user(email, password)
        return jsonify({"email": user_created.email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
    abort(401)


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """Log user out"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(location="/")
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """get user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", strict_slashes=False, methods=["POST"])
def reset_pwd():
    """reset password logic"""
    email = request.form.get("email")
    try:
        user = AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


@app.route("/reset_password", strict_slashes=False, methods=["PUT"])
def update_pwd():
    """handle updating user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
