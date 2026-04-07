from flask import Blueprint, request, jsonify
from models.new_referral_model import NewReferral
from database.db import db

doctor_side_referral_bp = Blueprint('doctor_side_referral_bp', __name__)

# ✅ GET REFERRAL (using unique_id)
@doctor_side_referral_bp.route('/doctor/referral/<int:referral_id>', methods=['GET'])
def get_referral(referral_id):
    print("DOCTOR API HIT")

    # 🔥 FIX: use unique_id
    referral = NewReferral.query.filter_by(unique_id=referral_id).first()

    if not referral:
        return jsonify({"message": "Referral not found"}), 404

    return jsonify({
        "message": "Success",
        "data": referral.to_dict()
    }), 200


# ✅ UPDATE REFERRAL (using unique_id)
@doctor_side_referral_bp.route('/doctor/referral/update', methods=['POST'])
def update_referral():
    data = request.get_json()

    referral_id = data.get("referral_id")
    suggestion = data.get("suggestion")
    precautions = data.get("precautions")

    # 🔥 FIX: use unique_id
    referral = NewReferral.query.filter_by(unique_id=referral_id).first()

    if not referral:
        return jsonify({"message": "Referral not found"}), 404

    referral.suggestion = suggestion
    referral.precautions = precautions

    db.session.commit()

    return jsonify({"message": "Updated successfully"}), 200