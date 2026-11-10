import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from ai_engine import analyze_skills, generate_roadmap

from models import User, Resume, Job, SkillMatch

from extensions import db, login_manager
from models import User

from werkzeug.utils import secure_filename
from resume_parser import extract_resume_text

from datetime import datetime


load_dotenv()

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "local-development-key-change-before-deployment"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skillbridge.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This email is already registered.", "error")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():

    if request.method == "POST":

        # Step 1: Get job description
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        # Step 2: Get uploaded resume
        resume_file = request.files.get("resume")

        # Step 3: Validate inputs
        if not resume_file or resume_file.filename == "":
            flash("Please upload your resume.", "error")
            return redirect(url_for("analysis"))

        if not job_description:
            flash("Please enter the job description.", "error")
            return redirect(url_for("analysis"))

        # Step 4: Validate file extension
        original_name = secure_filename(resume_file.filename)
        extension = os.path.splitext(original_name)[1].lower()

        if extension not in [".pdf", ".docx"]:
            flash("Only PDF and DOCX files are allowed.", "error")
            return redirect(url_for("analysis"))

        # Step 5: Generate unique filename
        unique_name = f"{uuid.uuid4().hex}{extension}"

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_name
        )

        try:

            # Step 6: Save uploaded resume
            resume_file.save(file_path)

            # Step 7: Extract resume text
            resume_text = extract_resume_text(file_path)

            if not resume_text:
                flash("No readable text found in your resume.", "error")
                return redirect(url_for("analysis"))

            # Step 8: Analyze resume skills
            result = analyze_skills(
                resume_text,
                job_description
            )

            # Step 9: Save resume information
            resume_record = Resume(
                user_id=current_user.id,
                filename=unique_name,
                extracted_text=resume_text
            )

            # Step 10: Save job information
            job_record = Job(
                title="Resume Skill Analysis",
                company="User Submitted Job",
                required_skills=", ".join(
                    result["required_skills"]
                ),
                description=job_description
            )

            db.session.add(resume_record)
            db.session.add(job_record)

            # Generate database IDs
            db.session.flush()

            # Step 11: Save skill match information
            match_record = SkillMatch(
                user_id=current_user.id,
                job_id=job_record.id,
                match_score=result["match_percentage"],
                matched_skills=", ".join(
                    result["matched_skills"]
                ),
                missing_skills=", ".join(
                    result["missing_skills"]
                )
            )

            db.session.add(match_record)

            # Step 12: Commit database records
            db.session.commit()

            # Step 13: Generate learning roadmap
            roadmap = generate_roadmap(
                result["missing_skills"]
            )

            # Step 14: Display results
            return render_template(
                "results.html",
                result=result,
                roadmap=roadmap
            )

        except Exception as error:

            # Rollback unsuccessful database transaction
            db.session.rollback()

            app.logger.exception(
                "Resume analysis failed"
            )

            flash(
                "Unable to analyze your resume. Please try again.",
                "error"
            )

            return redirect(url_for("analysis"))

    # GET request
    return render_template("analysis.html")


app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)        

@app.route("/history")
@login_required
def history():

    records = (
        db.session.query(
            SkillMatch,
            Job.title,
            Job.company
        )
        .join(Job, SkillMatch.job_id == Job.id)
        .filter(SkillMatch.user_id == current_user.id)
        .order_by(SkillMatch.id.desc())
        .all()
    )

    return render_template(
        "history.html",
        records=records
    )



if __name__ == "__main__":
    app.run(debug=True)