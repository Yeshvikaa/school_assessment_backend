from flask import Blueprint, jsonify
from models.user_model import User

counselor_bp = Blueprint('counselor_bp', __name__)

# ==============================
# GET ALL COUNSELORS (overview)
# ==============================
@counselor_bp.route('/api/counselors', methods=['GET'])
def get_counselors():
    try:
        counselors = User.query.filter_by(role="counselor").all()

        result = []
        for c in counselors:
            result.append({
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "experience": c.years_exp if c.years_exp else "0",
                "initial": c.name[0].upper() if c.name else "C"
            })

        return jsonify({
            "success": True,
            "counselors": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ==============================
# GET COUNSELOR DETAILS BY ID
# ==============================
@counselor_bp.route('/api/counselor/<int:id>', methods=['GET'])
def get_counselor_details(id):
    try:
        counselor = User.query.filter_by(id=id, role="counselor").first()

        if not counselor:
            return jsonify({
                "success": False,
                "message": "Counselor not found"
            }), 404

        data = {
            "id": counselor.id,
            "name": counselor.name,
            "email": counselor.email,
            "phone": counselor.phone,
            "age": counselor.age,
            "qualification": counselor.qualification,
            "school": counselor.school,
            "years_exp": counselor.years_exp,
            "security_destination": counselor.security_destination,
            "security_food": counselor.security_food,
            "security_hobby": counselor.security_hobby
        }

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server Error: {str(e)}"
        }), 500