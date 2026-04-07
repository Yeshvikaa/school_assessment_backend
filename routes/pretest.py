from flask import Blueprint, request, jsonify
from database.db import db
from models.pretest_model import PretestResult
import json

pretest_bp = Blueprint('pretest', __name__)

# =========================
# QUESTIONS DATA
# =========================
questions = {
    "section1": [
        {
            "question": "Which behavioral pattern suggests neurodevelopmental disorder?",
            "options": [
                "Refusal after bullying",
                "Difficulty adjusting to schedule",
                "Mood changes during exams",
                "Fatigue after PE"
            ],
            "answer": 1
        },
        {
            "question": "Student sudden underachievement — first factor?",
            "options": [
                "Medical condition",
                "Family stress",
                "Depressive episode",
                "Bullying"
            ],
            "answer": 2
        },
        {
            "question": "SLD vs poor performance?",
            "options": [
                "Only under stress",
                "Only verbal",
                "Persists despite normal IQ",
                "Disappears with homework"
            ],
            "answer": 2
        },
        {
            "question": "Untreated childhood depression leads to?",
            "options": [
                "Less competition",
                "Antisocial traits",
                "Chronic mood disorders",
                "Poor handwriting"
            ],
            "answer": 2
        },
        {
            "question": "Why structured observation?",
            "options": [
                "Evaluate growth",
                "Remove academic testing",
                "Capture real-time behavior",
                "Ensure discipline"
            ],
            "answer": 2
        }
    ],

    "section2": [
        {
            "question": "Discussing suicide in schools?",
            "options": [
                "Avoid topic",
                "Open discussion reduces risk",
                "Only clinical",
                "Teachers only"
            ],
            "answer": 1
        },
        {
            "question": "Ignoring emotional issues unless severe?",
            "options": [
                "Focus resources",
                "Miss anxiety/depression",
                "Better discipline",
                "Best practice"
            ],
            "answer": 1
        },
        {
            "question": "Children too young for emotions?",
            "options": [
                "Age appropriate",
                "Protects stress",
                "Limits emotional literacy",
                "Self solve"
            ],
            "answer": 2
        },
        {
            "question": "Open emotional discussion helps?",
            "options": [
                "Uncomfortable",
                "Increase problems",
                "Reduce stigma",
                "Shift responsibility"
            ],
            "answer": 2
        },
        {
            "question": "Academic issues = motivation?",
            "options": [
                "Better management",
                "Miss disabilities",
                "Peer discipline",
                "Time saving"
            ],
            "answer": 1
        },
        {
            "question": "Referral as last resort?",
            "options": [
                "Strengthens autonomy",
                "Supports confidentiality",
                "Delays intervention",
                "Reduces dependency"
            ],
            "answer": 2
        },
        {
            "question": "No support expectation?",
            "options": [
                "Faster integration",
                "More independence",
                "Miss inclusive intervention",
                "Better time management"
            ],
            "answer": 2
        },
        {
            "question": "Emotion discussion reduces discipline?",
            "options": [
                "Encourages expression",
                "Misunderstands mental health",
                "Improves regulation",
                "Structured routine"
            ],
            "answer": 1
        },
        {
            "question": "Inclusive attitude?",
            "options": [
                "Separate students",
                "Treat same",
                "Support helps thrive",
                "Avoid intervention"
            ],
            "answer": 2
        },
        {
            "question": "Handling parent concern?",
            "options": [
                "Wait for parents",
                "Sensitive early discussion",
                "Let teacher handle",
                "Wait for severity"
            ],
            "answer": 1
        }
    ],

    "section3": [
        {
            "question": "Withdrawn student first step?",
            "options": [
                "Ask classmates",
                "Write feelings",
                "Observe & document",
                "Wait"
            ],
            "answer": 2
        },
        {
            "question": "ADHD disruption next step?",
            "options": [
                "Suspend",
                "More breaks",
                "Movement breaks",
                "Written only"
            ],
            "answer": 2
        },
        {
            "question": "Sensory distress intervention?",
            "options": [
                "Discipline",
                "Force exposure",
                "Quiet space",
                "Send home"
            ],
            "answer": 2
        },
        {
            "question": "Suspected SLD action?",
            "options": [
                "Repeat year",
                "Multi-sensory + referral",
                "Remove work",
                "Tutoring"
            ],
            "answer": 1
        },
        {
            "question": "Repetitive behavior next step?",
            "options": [
                "Group games",
                "Structured observation",
                "Change seat",
                "IQ test"
            ],
            "answer": 1
        }
    ]
}


# =========================
# GET QUESTIONS API
# =========================
@pretest_bp.route('/get_pretest', methods=['GET'])
def get_pretest():
    return jsonify({
        "status": "success",
        "data": questions
    })


# =========================
# SUBMIT TEST API
# =========================
@pretest_bp.route('/submit_pretest', methods=['POST'])
def submit_pretest():
    try:
        data = request.get_json()

        email = data.get("email")
        user_answers = data.get("answers", [])

        # Combine all questions
        all_questions = (
            questions["section1"] +
            questions["section2"] +
            questions["section3"]
        )

        score = 0
        processed_answers = []

        for i, question in enumerate(all_questions):
            if i < len(user_answers):
                selected = user_answers[i]
                correct = question["answer"]

                is_correct = selected == correct
                if is_correct:
                    score += 1

                processed_answers.append({
                    "question": question["question"],
                    "selected_option": selected,
                    "selected_text": question["options"][selected] if selected < len(question["options"]) else None,
                    "correct_option": correct,
                    "correct_text": question["options"][correct],
                    "is_correct": is_correct
                })
            else:
                processed_answers.append({
                    "question": question["question"],
                    "selected_option": None,
                    "selected_text": None,
                    "correct_option": question["answer"],
                    "correct_text": question["options"][question["answer"]],
                    "is_correct": False
                })

        total_questions = len(all_questions)

        # Save to DB
        result = PretestResult(
            email=email,
            answers=json.dumps(processed_answers),
            score=score,
            total=total_questions
        )

        db.session.add(result)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Test submitted successfully",
            "score": score,
            "total": total_questions,
            "attempted": len(user_answers)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500