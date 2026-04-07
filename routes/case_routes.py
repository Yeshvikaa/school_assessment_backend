from flask import Blueprint, request, jsonify
from database.db import db
from models.case_model import CaseScenarioResult
import json

case_bp = Blueprint('case', __name__)

# =========================
# CASE SCENARIOS DATA
# =========================

case_scenarios = [
    {
        "id": 1,
        "scenario": "Krishna, a 11-year-old, often submits homework with only the first page completed and the rest left blank. In lessons, he blurts out unrelated facts, fidgets constantly, and sometimes starts doodling while others are reading aloud. He frequently misplaces his stationery and seems unable to follow multi-step instructions, jumping from one task to another. His teacher finds his interruptions disruptive, while his parents describe evenings filled with unfinished chores, misplaced belongings, and restless pacing around the house. A recent incident where he knocked over a younger student while running in the corridor has added to concerns about his impulsivity.",
        "questions": [
            "Describe the features of the psychological problem in the student",
            "What are the concerns by teacher and parent?",
            "What potential psychological issue could the student have?",
            "What intervention or support strategies could be done?"
        ]
    },
    {
        "id": 2,
        "scenario": "Arjun, a 15-year-old, has been suspended twice this term for vandalising the school restroom with graffiti. Teachers report that he openly mocks them in class and deliberately breaks rules. On the football field, he was involved in an incident where he pushed another student, causing injury, and showed no remorse when confronted. At home, his parents are worried about his late nights, frequent lying about his whereabouts, and an incident where he took money from his mother’s purse. Recently, they discovered he had been selling his younger cousin’s toys online without permission.",
        "questions": [
            "Describe the features of the psychological problem in the student",
            "What are the concerns by teacher and parent?",
            "What potential psychological issue could the student have?",
            "What intervention or support strategies could be done?"
        ]
    },
    {
        "id": 3,
        "scenario": "Meena, an 8-year-old, has begun missing school at least twice a week. On school mornings, she cries, clings to her mother, and complains of headaches. Her teacher reports that when she does attend, she is quiet and withdrawn, falling behind in her work. At home, her parents say she returns to her usual cheerful self once she is allowed to stay home. They recall that her reluctance began after older children teased her on the school bus. Now she insists that her mother must walk her into the classroom and stay until lessons begin.",

        "questions": [
            "Describe the features of the psychological problem in the student",
            "What are the concerns by teacher and parent?",
            "What potential psychological issue could the student have?",
            "What intervention or support strategies could be done?"
        ]
    }
]

# =========================
# GET CASE SCENARIOS
# =========================
@case_bp.route('/get_cases', methods=['GET'])
def get_cases():
    return jsonify({
        "status": "success",
        "data": case_scenarios
    })


# =========================
# SUBMIT CASE ANSWERS
# =========================
@case_bp.route('/submit_cases', methods=['POST'])
def submit_cases():
    try:
        data = request.get_json()

        email = data.get("email")
        answers = data.get("answers")  # List of all answers

        result = CaseScenarioResult(
            email=email,
            answers=json.dumps(answers)
        )

        db.session.add(result)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Case scenarios submitted successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500