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
            "question": "Which behavioral pattern in a student most strongly suggests an underlying neurodevelopmental disorder rather than situational stress?",
            "options": [
                "Refusal after bullying",
                "Difficulty adjusting to schedule",
                "Mood changes during exams",
                "Fatigue after PE"
            ],
            "answer": 1
        },
        {
            "question": "A student with a history of academic success has suddenly started showing signs of underachievement, marked by increased irritability, social withdrawal, and complaints of physical discomfort. Which factor should be explored first in understanding this sudden change in behavior?",
            "options": [
                "Medical condition",
                "Family stress",
                "Depressive episode",
                "Bullying"
            ],
            "answer": 2
        },
        {
            "question": "What distinguishes Specific Learning Disability (SLD) from general poor academic performance?",
            "options": [
                "Only under stress",
                "Only verbal",
                "Persists despite normal IQ",
                "Disappears with homework"
            ],
            "answer": 2
        },
        {
            "question": "Which of the following best explains the long-term impact of untreated childhood depression?",
            "options": [
                "Less competition",
                "Antisocial traits",
                "Chronic mood disorders",
                "Poor handwriting"
            ],
            "answer": 2
        },
        {
            "question": "Why is structured observation preferred in early identification of emotional issues in school children?",
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
            "question": "Some counselors worry that addressing suicide in schools may increase the risk of such behavior. According to recent perspectives, the more accurate understanding is:",
            "options": [
                "Avoid topic",
                "Open discussion reduces risk",
                "Only clinical",
                "Teachers only"
            ],
            "answer": 1
        },
        {
            "question": "A counselor believes that emotional health concerns should only be addressed if a student shows severe behavioral issues. This belief may:",
            "options": [
                "Focus resources",
                "Miss anxiety/depression",
                "Better discipline",
                "Best practice"
            ],
            "answer": 1
        },
        {
            "question": "A counselor avoids discussing emotional well-being because they assume children “are too young to talk about such things.” This belief:",
            "options": [
                "Age appropriate",
                "Protects stress",
                "Limits emotional literacy",
                "Self solve"
            ],
            "answer": 2
        },
        {
            "question": " A counselor who encourages open discussions about emotional stress in class is most likely to: ",
            "options": [
                "Uncomfortable",
                "Increase problems",
                "Reduce stigma",
                "Shift responsibility"
            ],
            "answer": 2
        },
        {
            "question": ".Believing that a child’s academic difficulties are purely motivational — without exploring emotional or cognitive causes — may result in:",
            "options": [
                "Better management",
                "Miss disabilities",
                "Peer discipline",
                "Time saving"
            ],
            "answer": 1
        },
        {
            "question": "If a counselor views referral to a mental health professional as a last resort, it may:",
            "options": [
                "Strengthens autonomy",
                "Supports confidentiality",
                "Delays intervention",
                "Reduces dependency"
            ],
            "answer": 2
        },
        {
            "question": "A belief that students with psychological issues should adjust to regular school routines without support may result in:",
            "options": [
                "Faster integration",
                "More independence",
                "Miss inclusive intervention",
                "Better time management"
            ],
            "answer": 2
        },
        {
            "question": ".If a counselor assumes that discussing emotions in school will reduce discipline and focus, this attitude:",
            "options": [
                "Encourages expression",
                "Misunderstands mental health",
                "Improves regulation",
                "Structured routine"
            ],
            "answer": 1
        },
        {
            "question": "Which of the following reflects an inclusive and growth-focused attitude?",
            "options": [
                "Separate students",
                "Treat same",
                "Support helps thrive",
                "Avoid intervention"
            ],
            "answer": 2
        },
        {
            "question": "A counselor worries that parents will react negatively to a mental health referral. Which attitude best balances concern and responsibility?",
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
            "question": "You observe a student displaying social withdrawal, frequent mood swings, and verbal expressions of hopelessness. What should be your first structured step?",
            "options": [
                "Ask classmates",
                "Write feelings",
                "Observe & document",
                "Wait"
            ],
            "answer": 2
        },
        {
            "question": "A student with ADHD is disrupting class repeatedly despite previous behavioral reinforcement. What should your next practical action include?",
            "options": [
                "Suspend",
                "More breaks",
                "Movement breaks",
                "Written only"
            ],
            "answer": 2
        },
        {
            "question": "When a child shows sensory distress and meltdown during assemblies, what immediate school-level intervention is appropriate?",
            "options": [
                "Discipline",
                "Force exposure",
                "Quiet space",
                "Send home"
            ],
            "answer": 2
        },
        {
            "question": "You suspect a student has Specific Learning Disability, but they are still in mainstream classes. What is your most appropriate course of action?",
            "options": [
                "Repeat year",
                "Multi-sensory + referral",
                "Remove work",
                "Tutoring"
            ],
            "answer": 1
        },
        {
            "question": "During play observation, a child repeats patterns, avoids interaction, and lines up objects. What is your practical next step?",
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