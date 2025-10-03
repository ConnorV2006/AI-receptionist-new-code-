import os
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# -------------------------------------------------
# App Config
# -------------------------------------------------
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"

from models import User, Role, Patient, Appointment, Note, Clinic, CallLog, MessageLog, AuditLog


# -------------------------------------------------
# User Loader
# -------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")

            # Redirect based on role
            if user.role and user.role.name == "superadmin":
                return redirect(url_for("superadmin_dashboard"))
            elif user.role and user.role.name == "receptionist":
                return redirect(url_for("receptionist_dashboard"))
            elif user.role and user.role.name == "doctor":
                return redirect(url_for("doctor_dashboard"))
            else:
                return redirect(url_for("dashboard"))  # fallback
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


# ---------------- Dashboard Redirect ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role and current_user.role.name == "superadmin":
        return redirect(url_for("superadmin_dashboard"))
    elif current_user.role and current_user.role.name == "receptionist":
        return redirect(url_for("receptionist_dashboard"))
    elif current_user.role and current_user.role.name == "doctor":
        return redirect(url_for("doctor_dashboard"))
    else:
        abort(403)


# ---------------- Superadmin Dashboard ----------------
@app.route("/dashboard/superadmin")
@login_required
def superadmin_dashboard():
    if not current_user.role or current_user.role.name != "superadmin":
        abort(403)

    users = User.query.all()
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(20).all()
    clinics = Clinic.query.all()

    return render_template("superadmin_dashboard.html", users=users, logs=logs, clinics=clinics)


# ---------------- Receptionist Dashboard ----------------
@app.route("/dashboard/receptionist")
@login_required
def receptionist_dashboard():
    if not current_user.role or current_user.role.name != "receptionist":
        abort(403)

    upcoming_appts = Appointment.query.order_by(Appointment.scheduled_for.asc()).limit(10).all()
    messages = MessageLog.query.order_by(MessageLog.created_at.desc()).limit(5).all()
    calls = CallLog.query.order_by(CallLog.created_at.desc()).limit(5).all()
    patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()

    return render_template(
        "receptionist_dashboard.html",
        appointments=upcoming_appts,
        messages=messages,
        calls=calls,
        patients=patients,
    )


# ---------------- Doctor Dashboard ----------------
@app.route("/dashboard/doctor")
@login_required
def doctor_dashboard():
    if not current_user.role or current_user.role.name != "doctor":
        abort(403)

    todays_appts = (
        Appointment.query.filter(
            Appointment.doctor_id == current_user.id,
            db.func.date(Appointment.scheduled_for) == date.today()
        )
        .order_by(Appointment.scheduled_for.asc())
        .all()
    )
    patients = Patient.query.filter_by(doctor_id=current_user.id).all()
    notes = Note.query.filter_by(doctor_id=current_user.id).order_by(Note.created_at.desc()).limit(5).all()

    return render_template(
        "doctor_dashboard.html",
        todays_appointments=todays_appts,
        patients=patients,
        notes=notes,
    )


# ---------------- View Patient ----------------
@app.route("/patients/<int:patient_id>")
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("patient_view.html", patient=patient)


# ---------------- Audit Log Helper ----------------
def log_action(user_id, action):
    log = AuditLog(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
