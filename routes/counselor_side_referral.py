from flask import Blueprint, jsonify
from models.new_referral_model import NewReferral

counselor_side_referral_bp = Blueprint('counselor_side_referral_bp', __name__)

# ✅ VIEW FULL REFERRAL (Read-only using unique_id)
@counselor_side_referral_bp.route('/counselor/referral/<int:referral_id>', methods=['GET'])
def get_referral_counselor(referral_id):
    try:
        # 🔥 FIX: use unique_id instead of id
        referral = NewReferral.query.filter_by(unique_id=referral_id).first()

        if not referral:
            return jsonify({"message": "Referral not found"}), 404

        return jsonify({
            "message": "Success",
            "data": referral.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500