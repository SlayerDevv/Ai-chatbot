from flask import Flask, request,jsonify
from app import app
from user.models import User

@app.route("/auth/signup", methods=["POST"])
def signup():
    print("Route triggered!")  # Check if route is hit

    data = request.json if request.is_json else request.form
    print("Data received: ", data)  # Check incoming data

    email = data.get('email')
    username = data.get('username')
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing required fields", "success": "false"}), 400

    return User().Signup(email=email, username=username, password=password)


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json if request.is_json else request.form
    email = data.get('email')
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields", "success": "false"}), 400

    return User().Login(email=email, password=password)

