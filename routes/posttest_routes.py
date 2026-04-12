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
            "question": "A student with a history of academic success has suddenly started showing signs of underachievement, marked by increased irritability, social withdrawal, and complaints of physical discomfort. Which factor should be explored first in understanding this sudden change in behavior?",
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
        },
        {
            "question": "Which of the following would be the clearest indicator for referring a student for possible Intellectual Disability (ID)?",
            "options": [
                "Avoids reading aloud due to fear of embarrassment",
                "Shows physical complaints like headaches during exams",
                "Struggles with basic academic skills despite repeated help and support",
                "Often breaks rules and shows defiance toward authority figures"
            ],
            "answer": 2
        },
        {
            "question": "A student frequently complains of headaches and stomachaches, yet medical evaluations show no physical cause. They also demonstrate a high level of perfectionism, are often anxious about making mistakes, and avoid group activities. What might be the underlying issue?",
            "options": [
                "A mood disorder with somatic symptoms",
                "Generalized anxiety disorder",
                "A primary somatic disorder with anxiety as a secondary feature",
                "A personality disorder with a focus on academic performance"
            ],
            "answer": 1
        },
        {
            "question": "A student consistently displays aggressive behavior towards others, takes pleasure in seeing others upset, and has a history of vandalism and rule-breaking. Despite frequent disciplinary actions, the behavior does not seem to improve. What is the most likely explanation for this behavior?",
            "options": [
                "Exposure to significant trauma or abuse leading to maladaptive coping",
                "A conduct disorder, with an emphasis on a lack of empathy for others",
                "A personality disorder, particularly antisocial personality traits",
                "A learned behavior based on observing aggressive role models"
            ],
            "answer": 1
        },
        {
            "question": "A student repeatedly complains of headaches and stomachaches with no medical basis, particularly during tests or presentations. This suggests:",
            "options": [
                "Social skills deficit",
                "Autism Spectrum traits",
                "Anxiety-related somatic symptoms",
                "Oppositional behavior"
            ],
            "answer": 2
        },
        {
            "question": "When evaluating the emotional wellbeing of a student who has been withdrawn and irritable for weeks, which method is most likely to provide a comprehensive understanding of their mental health?",
            "options": [
                "Direct interviews with the student’s peers to assess social interactions",
                "A series of self-reported questionnaires assessing mood and behavior",
                "A combination of teacher observations, parental reports, and a structured psychological assessment",
                "Observation of the student’s behavior during unstructured play or free time"
            ],
            "answer": 2
        }
    ],

    "section2": [
        {
            "question": "Some counselors worry that addressing suicide in schools may increase the risk of such behavior. According to recent perspectives, the more accurate understanding is:",
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
        },
        {
            "question": "If a counselor views referral to a mental health professional as a last resort, it may:",
            "options": [
                "Strengthen school autonomy",
                "Support student confidentiality",
                "Delay access to early intervention",
                "Reduce dependency on outside help"
            ],
            "answer": 2
        },
        {
            "question": "A belief that students with psychological issues should adjust to regular school routines without support may result in:",
            "options": [
                "Faster classroom integration",
                "Greater independence and resilience",
                "Missed opportunities for inclusive interventions",
                "More effective time management for teachers"
            ],
            "answer": 2
        },
        {
            "question": "If a counselor assumes that discussing emotions in school will reduce discipline and focus, this attitude:",
            "options": [
                "Encourages emotional expression",
                "Misunderstands the role of mental health in academic success",
                "Enhances behavior regulation strategies",
                "Aligns with structured classroom routines"
            ],
            "answer": 1
        },
        {
            "question": "Which of the following reflects an inclusive and growth-focused attitude?",
            "options": [
                "Students with psychological needs should be separated to avoid disrupting others.",
                "All students should be treated the same, regardless of their difficulties.",
                "With support, most children can learn and thrive in regular classrooms.",
                "It’s better to avoid interventions that highlight a child’s issues."
            ],
            "answer": 2
        },
        {
            "question": "A counselor worries that parents will react negatively to a mental health referral. Which attitude best balances concern and responsibility?",
            "options": [
                "Unless parents ask, I won’t bring it up.",
                "Early conversations with sensitivity can help families understand and accept support.",
                "Let the teacher talk to them first.",
                "It’s better to wait until the problem becomes more obvious."
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
        },
        {
            "question": "A child is constantly failing to follow classroom routines and shows signs of low IQ and adaptive delays. What’s the most appropriate intervention plan?",
            "options": [
                "Introduce advanced academic material to build stimulation",
                "Use repetitive instructions with peer mentorship and routine training",
                "Refer immediately to a behavior therapist",
                "Shift the student to home-schooling"
            ],
            "answer": 1
        },
        {
            "question": "You observe a student bullying peers, skipping classes, and showing no empathy. After repeated interventions fail, your next best action is to:",
            "options": [
                "Request a parent-teacher meeting and enforce detention",
                "Refer to psychiatrist for conduct evaluation and intervention planning",
                "Let the behavior pass unless violence occurs",
                "Place them in special education directly"
            ],
            "answer": 1
        },
        {
            "question": "A student with anxiety avoids tests and complains of stomachaches before class. Which intervention aligns with best school-based practice?",
            "options": [
                "Use relaxation techniques and provide extended time for tasks",
                "Remove them from all performance-based assessments",
                "Enforce timed exams to train their stamina",
                "Ignore complaints unless they faint or vomit"
            ],
            "answer": 0
        },
        {
            "question": "What is the best way to assess if classroom behavior is due to emotional distress or a neurological condition?",
            "options": [
                "Monitor performance in only one subject",
                "Use teacher interviews, peer analysis, and structured observations",
                "Assign the child to remedial tuition",
                "Wait to see long-term academic scores"
            ],
            "answer": 1
        },
        {
            "question": "What should a counselor do when a child repeatedly says they feel unloved and wants to disappear?",
            "options": [
                "Reassure them it’s just teenage mood",
                "Ask parents to restrict screen time",
                "Document the expression, assess risk, and refer for mental health evaluation",
                "Suggest they speak to a friend"
            ],
            "answer": 2
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