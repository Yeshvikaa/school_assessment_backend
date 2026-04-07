from flask import Flask
from flask_cors import CORS
from database.db import db
from config import Config


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # =========================
    # REGISTER BLUEPRINTS
    # =========================

    # AUTH (Signup/Login)
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # PRETEST
    from routes.pretest import pretest_bp
    app.register_blueprint(pretest_bp, url_prefix='/api')

    # POSTTEST ✅ (IMPORTANT FIX)
    from routes.posttest_routes import posttest_bp
    app.register_blueprint(posttest_bp, url_prefix='/api')

    # MODULES
    from routes.modules_routes import modules_bp
    app.register_blueprint(modules_bp, url_prefix='/api/modules')

    # CASES
    from routes.case_routes import case_bp
    app.register_blueprint(case_bp, url_prefix='/api/cases')

    # Register referral routes
    from routes.new_referral_routes import new_referral_bp
    app.register_blueprint(new_referral_bp, url_prefix='/api')

    from routes.view_referral_routes import view_referral_bp
    app.register_blueprint(view_referral_bp)

    from routes.profile_routes import profile_bp
    app.register_blueprint(profile_bp)

    from routes.doctor_counselor_referral import doctor_referral_bp
    app.register_blueprint(doctor_referral_bp, url_prefix='/api')

    from routes.view_referrals_doctor import view_referrals_doctor_bp
    app.register_blueprint(view_referrals_doctor_bp)

    from routes.doctor_side_referral import doctor_side_referral_bp
    app.register_blueprint(doctor_side_referral_bp, url_prefix='/api')

    from routes.counselor_side_referral import counselor_side_referral_bp
    app.register_blueprint(counselor_side_referral_bp, url_prefix='/api')

    from routes.chat_routes import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from routes.counselor_routes import counselor_bp
    app.register_blueprint(counselor_bp)

    from routes.parent_routes import parent_bp
    app.register_blueprint(parent_bp)
    # print("📌 REGISTERED ROUTES:")
    # print(app.url_map)  # this will show all routes
    # (Optional future routes)
    # from routes.progress_routes import progress_bp
    # app.register_blueprint(progress_bp, url_prefix='/api/progress')

    # from routes.user_routes import user_bp
    # app.register_blueprint(user_bp, url_prefix='/api/user')

    # from routes.dashboard_routes import dashboard_bp
    # app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    return app


# =========================
# APP START
# =========================

app = create_app()

# Create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)