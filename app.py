import os
from datetime import datetime, date
import sqlalchemy as sa
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from models import User, Patient, Appointment, CallLog, MessageLog, Clinic, AuditLog, Note

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route with role redirects
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            if user.role and user.role.name == "superadmin":
                return redirect(url_for("superadmin_dashboard"))
            elif user.role and user.role.name == "receptionist":
                return redirect(url_for("receptionist_dashboard"))
            elif user.role and user.role.name == "doctor":
                return redirect(url_for("doctor_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# Fallback dashboard redirect
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

# Superadmin dashboard
@app.route("/dashboard/superadmin")
@login_required
def superadmin_dashboard():
    if not current_user.role or current_user.role.name != "superadmin":
        abort(403)

    users_count = User.query.count()
    clinics_count = Clinic.query.count()
    appointments_count = Appointment.query.count()
    audit_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()
    audit_logs_count = AuditLog.query.count()

    return render_template(
        "superadmin_dashboard.html",
        users_count=users_count,
        clinics_count=clinics_count,
        appointments_count=appointments_count,
        audit_logs=audit_logs,
        audit_logs_count=audit_logs_count,
    )

# Receptionist dashboard
@app.route("/dashboard/receptionist")
@login_required
def receptionist_dashboard():
    if not current_user.role or current_user.role.name != "receptionist":
        abort(403)

    clinic = Clinic.query.first()

    patients_count = Patient.query.filter_by(clinic_id=clinic.id).count()
    appointments_count = Appointment.query.join(Patient).filter(Patient.clinic_id==clinic.id).count()
    messages_count = MessageLog.query.filter_by(clinic_id=clinic.id).count()

    appointments = Appointment.query.join(Patient).filter(Patient.clinic_id==clinic.id).order_by(Appointment.scheduled_for.asc()).limit(5).all()
    calls = CallLog.query.filter_by(clinic_id=clinic.id).order_by(CallLog.created_at.desc()).limit(5).all()
    messages = MessageLog.query.filter_by(clinic_id=clinic.id).order_by(MessageLog.created_at.desc()).limit(5).all()

    return render_template(
        "receptionist_dashboard.html",
        patients_count=patients_count,
        appointments_count=appointments_count,
        messages_count=messages_count,
        appointments=appointments,
        calls=calls,
        messages=messages,
    )

# Doctor dashboard
@app.route("/dashboard/doctor")
@login_required
def doctor_dashboard():
    if not current_user.role or current_user.role.name != "doctor":
        abort(403)

    todays_appointments = (
        Appointment.query.filter(
            Appointment.doctor_id == current_user.id,
            sa.func.date(Appointment.scheduled_for) == date.today()
        )
        .order_by(Appointment.scheduled_for.asc())
        .all()
    )

    patients = Patient.query.filter_by(doctor_id=current_user.id).all()
    notes = (
        Note.query.filter_by(doctor_id=current_user.id)
        .order_by(Note.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "doctor_dashboard.html",
        todays_appointments=todays_appointments,
        patients=patients,
        notes=notes
    )

if __name__ == "__main__":
    app.run(debug=True)
