from flask import Blueprint, request, jsonify
from models.new_referral_model import NewReferral

view_referral_bp = Blueprint('view_referral_bp', __name__)

@view_referral_bp.route('/api/view-referrals', methods=['POST'])
def view_referrals():
    data = request.get_json()

    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    try:
        referrals = NewReferral.query.filter_by(counselor_email=email).all()

        if not referrals:
            return jsonify({
                "message": "No referrals found",
                "data": []
            }), 200

        result = []
        for ref in referrals:
            result.append({
                "referral_id": ref.unique_id,   # ✅ FIXED (IMPORTANT)
                "name": ref.name,
                "initial": ref.name[0].upper() if ref.name else "",
                "reason": ref.reason,
                "status": "Replied"
            })

        return jsonify({
            "message": "Success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500