# routes/view_referrals_doctor.py

from flask import Blueprint, request, jsonify
from models.new_referral_model import NewReferral

view_referrals_doctor_bp = Blueprint('view_referrals_doctor_bp', __name__)

@view_referrals_doctor_bp.route('/api/view-referrals-doctor', methods=['POST'])
def view_referrals_doctor():

    try:
        # 🔥 FIX: enforce order
        referrals = NewReferral.query.order_by(NewReferral.unique_id.asc()).all()

        if not referrals:
            return jsonify({
                "message": "No referrals found",
                "data": []
            }), 200

        result = []
        for ref in referrals:
            result.append({
                
                "referral_id": ref.unique_id,  # ✅ MUST

                "initial": ref.name[0].upper() if ref.name else "",
                "name": ref.name,
                "reason": ref.reason,
                "status": "Pending" if not ref.suggestion else "Replied"
            })

        return jsonify({
            "message": "Success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500