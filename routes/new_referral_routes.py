from flask import Blueprint, request, jsonify
from models.new_referral_model import NewReferral
from database.db import db

new_referral_bp = Blueprint('new_referral_bp', __name__)

@new_referral_bp.route('/referral', methods=['POST'])
def add_referral():
    data = request.get_json()

    # ✅ Updated validation (added counselor_email)
    if not data.get('unique_id') or not data.get('name') or not data.get('counselor_email'):
        return jsonify({
            'status': 'error',
            'message': 'Unique ID, Name and Counselor Email are required'
        }), 400

    try:
        referral = NewReferral(
            unique_id=data.get('unique_id'),
            name=data.get('name'),
            age=data.get('age'),
            student_class=data.get('student_class'),
            address=data.get('address'),
            reason=data.get('reason'),
            behavior=data.get('behavior'),
            academic=data.get('academic'),
            counselor_email=data.get('counselor_email')  # ✅ added
        )

        db.session.add(referral)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Referral submitted successfully',
            'data': referral.to_dict()
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500