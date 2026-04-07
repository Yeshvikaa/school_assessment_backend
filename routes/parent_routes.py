from flask import Blueprint, request, jsonify
from models.user_model import User
from models.new_referral_model import NewReferral   # ✅ make sure this exists

parent_bp = Blueprint('parent_bp', __name__)

# ==========================================
# GET PARENT DASHBOARD DATA
# ==========================================
@parent_bp.route('/api/parent/dashboard', methods=['POST'])
def parent_dashboard():
    try:
        data = request.get_json()

        email = data.get("email")

        if not email:
            return jsonify({
                "status": "error",
                "message": "Email is required"
            }), 400

        # 🔍 STEP 1: FIND PARENT
        parent = User.query.filter_by(email=email, role="parent").first()

        if not parent:
            return jsonify({
                "status": "error",
                "message": "Parent not found"
            }), 404

        # 🔍 STEP 2: GET STUDENT ID
        student_id = parent.student_id

        if not student_id:
            return jsonify({
                "status": "error",
                "message": "Student ID not linked"
            }), 400

        # 🔍 STEP 3: FIND REFERRAL USING UNIQUE_ID
        referral = NewReferral.query.filter_by(unique_id=student_id).first()

        if not referral:
            return jsonify({
                "status": "error",
                "message": "No referral found for this student"
            }), 404

        # ✅ STEP 4: RETURN DATA
        return jsonify({
            "status": "success",
            "role": "parent",
            "data": {
                "id": referral.id,
                "name": referral.name,
                "age": referral.age,
                "student_class": referral.student_class,
                "academic": referral.academic,
                "behavior": referral.behavior,
                "reason": referral.reason,
                "suggestion": referral.suggestion,
                "precautions": referral.precautions,
                "doctor_email": referral.doctor_email,
                "counselor_email": referral.counselor_email,
                "address": referral.address,
                "unique_id": referral.unique_id
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500