import uuid
from passlib.hash import pbkdf2_sha256
from app import db
from flask import jsonify
import uuid

class User:
    def Signup(self, username, email, password):
        
        if db.users.find_one({ "email": email}):
            return jsonify({"error": "Email already in use", "success": "false"}), 400
        
        if db.users.find_one({"username": username}):
            return jsonify({"error": "Username already in use", "success": "false"}), 400
        
        user = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "password":  pbkdf2_sha256.hash(password),
            "conversations_ids": []
        }
        db.users.insert_one(user)
        return jsonify({"error": "", "success": "true", "data": user}), 200    
    def Login(self, email, password):
        if not db.users.find_one({"email": email}):
            return jsonify({"error": "Email not found", "success": "false"}), 400
        
        user = db.users.find_one({"email": email})
        
        if not pbkdf2_sha256.verify(password, user["password"]):
            return jsonify({"error": "Invalid password", "success": "false"}), 400
        
        return jsonify({"error": "", "success": "true", "data": user}), 200