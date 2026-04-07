#doctor_counselor_referral
from flask import Blueprint, request, jsonify
from models.new_referral_model import NewReferral
from database.db import db

doctor_referral_bp = Blueprint('doctor_referral_bp', __name__)

# ✅ Get referral by ID (for both doctor & counselor)
@doctor_referral_bp.route('/referral/<int:referral_id>', methods=['GET'])
def get_referral(referral_id):
    user_role = request.args.get('role')  # 'doctor' or 'counselor'
    referral = NewReferral.query.get(referral_id)
    if not referral:
        return jsonify({'status': 'error', 'message': 'Referral not found'}), 404

    return jsonify({
        'status': 'success',
        'data': referral.to_dict(),
        'role': user_role
    })

# ✅ Update suggestion & precautions (only doctor)
@doctor_referral_bp.route('/referral/<int:referral_id>', methods=['PUT'])
def update_referral(referral_id):
    data = request.get_json()
    user_role = data.get('role')  # must be 'doctor' to update
    if user_role != 'doctor':
        return jsonify({'status': 'error', 'message': 'Only doctors can update suggestion and precautions'}), 403

    referral = NewReferral.query.get(referral_id)
    if not referral:
        return jsonify({'status': 'error', 'message': 'Referral not found'}), 404

    # Only update suggestion and precautions
    referral.suggestion = data.get('suggestion', referral.suggestion)
    referral.precautions = data.get('precautions', referral.precautions)
    referral.doctor_email = data.get('doctor_email', referral.doctor_email)

    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Referral updated successfully',
            'data': referral.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500