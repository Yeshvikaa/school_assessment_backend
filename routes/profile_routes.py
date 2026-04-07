from flask import Blueprint, request, jsonify
from database.db import db
from models.user_model import User

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/get_profile', methods=['GET'])
def get_profile():
    email = request.args.get('email')

    if not email:
        return jsonify({"status": "error", "message": "Email required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "department": user.qualification,   # ✅ mapped
            "experience": user.years_exp        # ✅ mapped
        }
    }), 200