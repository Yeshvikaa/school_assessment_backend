from flask import Blueprint, request, jsonify
from models.chat_message import ChatMessage
from models.new_referral_model import NewReferral
from database.db import db

print("🔥 chat_routes LOADED")
chat_bp = Blueprint('chat_bp', __name__)

# ✅ SEND MESSAGE
@chat_bp.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()

        referral_unique_id = data.get('referral_unique_id')
        sender_email = data.get('sender_email')
        message = data.get('message')

        # validation
        if not referral_unique_id or not sender_email or not message:
            return jsonify({"error": "Missing required fields"}), 400

        # find referral
        referral = NewReferral.query.filter_by(unique_id=referral_unique_id).first()

        if not referral:
            return jsonify({"error": "Referral not found"}), 404

        # decide receiver
        if sender_email == referral.doctor_email:
            receiver_email = referral.counselor_email
        elif sender_email == referral.counselor_email:
            receiver_email = referral.doctor_email
        else:
            return jsonify({"error": "Sender not part of this referral"}), 403

        # create message
        new_msg = ChatMessage(
            referral_unique_id=referral_unique_id,
            sender_email=sender_email,
            receiver_email=receiver_email,
            message=message
        )

        db.session.add(new_msg)
        db.session.commit()

        return jsonify({
            "message": "Message sent successfully",
            "data": new_msg.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ GET ALL MESSAGES FOR A REFERRAL
@chat_bp.route('/get-messages/<int:referral_unique_id>', methods=['GET'])
def get_messages(referral_unique_id):
    try:
        messages = ChatMessage.query.filter_by(
            referral_unique_id=referral_unique_id
        ).order_by(ChatMessage.timestamp.asc()).all()

        return jsonify([msg.to_dict() for msg in messages]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ OPTIONAL: DELETE CHAT (for testing)
@chat_bp.route('/delete-chat/<int:referral_unique_id>', methods=['DELETE'])
def delete_chat(referral_unique_id):
    try:
        ChatMessage.query.filter_by(
            referral_unique_id=referral_unique_id
        ).delete()

        db.session.commit()

        return jsonify({"message": "Chat deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500