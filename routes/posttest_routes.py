from flask import Blueprint, request, jsonify
from database.db import db
from models.posttest_model import PosttestResult
import json

posttest_bp = Blueprint('posttest', __name__)

# =========================
# POSTTEST QUESTIONS
# =========================
questions = {
    "section1": [
        {
            "question": "Which behavioral pattern in a student most strongly suggests an underlying neurodevelopmental disorder rather than situational stress?",
            "options": [
                "Refusal to attend school after a bullying incident",
                "Difficulty adjusting to sudden changes in class schedule",
                "Mood changes during examination periods",
                "Fatigue following physical education class"
            ],
            "answer": 1
        },
        {
            "question": "A student with a history of academic success has suddenly started showing signs of underachievement, marked by increased irritability, social withdrawal, and complaints of physical discomfort. Which factor should be explored first?",
            "options": [
                "A medical condition, such as chronic pain or gastrointestinal issues",
                "A sudden shift in family dynamics, possibly indicating stress at home",
                "A possible depressive episode manifesting as somatic complaints",
                "A desire to avoid school due to bullying or peer rejection"
            ],
            "answer": 2
        },
        {
            "question": "What distinguishes Specific Learning Disability (SLD) from general poor academic performance?",
            "options": [
                "It occurs only when children are under stress",
                "It affects only verbal communication",
                "It persists despite adequate instruction and normal intelligence",
                "It disappears with additional homework"
            ],
            "answer": 2
        },
        {
            "question": "Which of the following best explains the long-term impact of untreated childhood depression?",
            "options": [
                "Reduced interest in academic competition",
                "Risk of developing antisocial traits",
                "Increased chance of developing chronic mood disorders",
                "Poor muscle coordination and handwriting"
            ],
            "answer": 2
        },
        {
            "question": "Why is structured observation preferred in early identification of emotional issues in school children?",
            "options": [
                "It helps evaluate physical growth milestones",
                "It eliminates the need for academic testing",
                "It captures behavioral patterns in real-time settings",
                "It ensures children follow school rules"
            ],
            "answer": 2
        }
    ],

    "section2": [
        {
            "question": "Some counselors worry that addressing suicide in schools may increase the risk of such behavior. The more accurate understanding is:",
            "options": [
                "It’s safer not to mention suicide at all",
                "Open, sensitive discussion with proper support reduces risk and stigma",
                "Suicide should only be discussed in clinical settings",
                "Only teachers should handle these conversations, not counselors"
            ],
            "answer": 1
        },
        {
            "question": "A counselor believes that emotional health concerns should only be addressed if a student shows severe behavioral issues. This belief may:",
            "options": [
                "Help focus resources on high-need cases",
                "Risk missing internalizing problems like anxiety or depression",
                "Encourage discipline-oriented approaches",
                "Reflect best practices in school-based triage"
            ],
            "answer": 1
        },
        {
            "question": "A counselor avoids discussing emotional well-being because they assume children “are too young to talk about such things.” This belief:",
            "options": [
                "Aligns with age-appropriate communication",
                "Protects students from stress",
                "Limits early emotional literacy and normalization of support",
                "Encourages children to solve their own problems"
            ],
            "answer": 2
        },
        {
            "question": "A counselor who encourages open discussions about emotional stress in class is most likely to:",
            "options": [
                "Make students uncomfortable",
                "Increase emotional problems",
                "Support help-seeking and reduce stigma",
                "Shift responsibility from parents to teachers"
            ],
            "answer": 2
        },
        {
            "question": "Believing that a child’s academic difficulties are purely motivational — without exploring emotional or cognitive causes — may result in:",
            "options": [
                "Improved classroom management",
                "Missed identification of learning disabilities or depression",
                "More effective peer discipline",
                "Better time management for teachers"
            ],
            "answer": 1
        }
    ],

    "section3": [
        {
            "question": "You observe a student displaying social withdrawal, frequent mood swings, and verbal expressions of hopelessness. What should be your first structured step?",
            "options": [
                "Inform classmates to offer more support",
                "Ask the student to write about their feelings as homework",
                "Initiate observation, document patterns, and prepare for referral",
                "Wait to see if symptoms resolve during exam periods"
            ],
            "answer": 2
        },
        {
            "question": "A student with ADHD is disrupting class repeatedly despite previous behavioral reinforcement. What should your next practical action include?",
            "options": [
                "Recommend suspension to enforce rules",
                "Increase unstructured break times",
                "Provide movement breaks and adjust instruction delivery",
                "Shift to written instruction only"
            ],
            "answer": 2
        },
        {
            "question": "When a child shows sensory distress and meltdown during assemblies, what immediate school-level intervention is appropriate?",
            "options": [
                "Refer for disciplinary review",
                "Force exposure to overcome avoidance",
                "Offer quiet sensory regulation space and visual schedule alternatives",
                "Send them home for the day"
            ],
            "answer": 2
        },
        {
            "question": "You suspect a student has Specific Learning Disability, but they are still in mainstream classes. What is your most appropriate course of action?",
            "options": [
                "Recommend repeating the academic year",
                "Initiate multi-sensory strategies and recommend screening referral",
                "Limit reading and writing assignments entirely",
                "Ask parents to increase home tutoring"
            ],
            "answer": 1
        },
        {
            "question": "During play observation, a child repeats patterns, avoids interaction, and lines up objects. What is your practical next step?",
            "options": [
                "Redirect the child to competitive group games",
                "Monitor over time using structured observation and teacher input",
                "Suggest changing their seating in class",
                "Conduct an immediate IQ test"
            ],
            "answer": 1
        }
    ]
}

# =========================
# GET POSTTEST QUESTIONS API
# =========================
@posttest_bp.route('/get_posttest', methods=['GET'])
def get_posttest():
    return jsonify({
        "status": "success",
        "data": questions
    })

# =========================
# SUBMIT POSTTEST API
# =========================
@posttest_bp.route('/submit_posttest', methods=['POST'])
def submit_posttest():
    try:
        data = request.get_json()
        email = data.get("email")
        user_answers = data.get("answers", [])

        all_questions = (
            questions["section1"] +
            questions["section2"] +
            questions["section3"]
        )

        score = 0
        processed_answers = []

        for i, question in enumerate(all_questions):
            selected = user_answers[i] if i < len(user_answers) else None
            correct = question["answer"]

            is_correct = selected == correct
            if is_correct:
                score += 1

            processed_answers.append({
                "question_no": i + 1,
                "question": question["question"],
                "selected_option": selected,
                "selected_text": question["options"][selected] if selected is not None else None,
                "correct_option": correct,
                "correct_text": question["options"][correct],
                "is_correct": is_correct
            })

        total_questions = len(all_questions)

        # Save result to DB
        result = PosttestResult(
            email=email,
            answers=json.dumps(processed_answers),
            score=score,
            total=total_questions
        )
        db.session.add(result)
        db.session.commit()

        return jsonify({
            "status": "success",
            "score": score,
            "total": total_questions,
            "answers": processed_answers
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500