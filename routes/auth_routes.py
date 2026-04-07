from flask import Blueprint, request, jsonify
from database.db import db
from models.user_model import User
from utils.hash_utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

# ---------------- SIGNUP ----------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    role = data.get("role")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    age = data.get("age")
    qualification = data.get("qualification")
    school = data.get("school")
    years_exp = data.get("years_exp")
    father_occ = data.get("father_occ")
    father_phone = data.get("father_phone")
    mother_occ = data.get("mother_occ")
    mother_phone = data.get("mother_phone")
    security_destination = data.get("security_destination")
    security_food = data.get("security_food")
    security_hobby = data.get("security_hobby")
    student_id = data.get("student_id")

    # validation
    if not role or not name or not email or not password:
        return jsonify({"status": "error", "message": "Role, Name, Email, Password are required"}), 400

    # check existing user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Email already exists"}), 409

    # hash password
    hashed_password = hash_password(password)

    # create user
    new_user = User(role, name, email, hashed_password, phone, age, qualification, school,
                    years_exp, father_occ, father_phone, mother_occ, mother_phone,
                    security_destination, security_food, security_hobby,student_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully"}), 201


# ---------------- LOGIN ----------------

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    # 🔥 CHECK EMAIL FROM SIGNUP TABLE
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    # 🔐 PASSWORD CHECK
    if not verify_password(user.password, password):
        return jsonify({
            "status": "error",
            "message": "Invalid password"
        }), 401

    # ✅ SUCCESS → SEND ROLE
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "role": user.role,
        "name": user.name,
        "email": user.email
    }), 200

