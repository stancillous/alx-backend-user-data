"""Basic Flask app"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
