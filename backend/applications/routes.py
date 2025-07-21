import os
from flask import current_app as app, jsonify, request, abort
from applications.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,JWTManager, jwt_required, get_jwt_identity, get_jwt, current_user
from datetime import datetime

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    full_name = data.get("full_name")
    address = data.get("address")
    pincode = data.get("pincode")
    password = data.get("password")

    if not username or not password or not full_name or not address or not pincode:
        return jsonify({"error": "All fields are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    user = User(
        username=username,
        full_name=full_name,
        address=address,
        pincode=pincode
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # First try user login
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.username, additional_claims={"role": "user"})
        return jsonify({"access_token": token, "role": "user"}), 200

    # Try admin login (hardcoded user)
    admin = Admin.query.filter_by(username=username).first()
    if admin and check_password_hash(admin.password, password):
        token = create_access_token(identity=admin.username, additional_claims={"role": "admin"})
        return jsonify({"access_token": token, "role": "admin"}), 200

    return jsonify({"error": "Wrong username or password"}), 401


@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful"}), 200