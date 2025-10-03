import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------
# App + Config
# -------------------------------------------------
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Patient, Appointment, AuditLog

# -------------------------------------------------
# Role decorator
# -------------------------------------------------
def role_required(allowed_roles):
    """Decorator to restrict access by role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_role" not in session:
                flash("You must be logged in to access this page.", "warning")
                return redirect(url_for("login"))
            if session["user_role"] not in allowed_roles:
                flash("You don’t have permission to access this page.", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("login"))

# ---------- Auth ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_role"] = user.role
            flash("Login successful!", "success")

            if user.role == "admin" or user.role == "superadmin":
                return redirect(url_for("admin_dashboard"))
            elif user.role == "doctor":
                return redirect(url_for("doctor_dashboard"))
            elif user.role == "nurse":
                return redirect(url_for("nurse_dashboard"))
            else:
                return redirect(url_for("receptionist_dashboard"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("auth/login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# ---------- Dashboards ----------
@app.route("/admin/dashboard")
@role_required(["admin", "superadmin"])
def admin_dashboard():
    return render_template("dashboards/admin_dashboard.html")

@app.route("/doctor/dashboard")
@role_required(["doctor", "superadmin"])
def doctor_dashboard():
    upcoming = Appointment.query.order_by(Appointment.date.asc()).limit(5).all()
    patients = Patient.query.limit(10).all()
    return render_template("dashboards/doctor_dashboard.html", upcoming_appointments=upcoming, patients=patients)

@app.route("/nurse/dashboard")
@role_required(["nurse", "superadmin"])
def nurse_dashboard():
    upcoming = Appointment.query.order_by(Appointment.date.asc()).limit(5).all()
    patients = Patient.query.limit(10).all()
    return render_template("dashboards/nurse_dashboard.html", upcoming_appointments=upcoming, patients=patients)

@app.route("/receptionist/dashboard")
@role_required(["receptionist", "superadmin"])
def receptionist_dashboard():
    upcoming = Appointment.query.order_by(Appointment.date.asc()).limit(5).all()
    patients = Patient.query.limit(10).all()
    return render_template("dashboards/receptionist_dashboard.html", upcoming_appointments=upcoming, patients=patients)

# ---------- Audit Logs ----------
@app.route("/audit/logs")
@role_required(["admin", "superadmin"])
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(50).all()
    return render_template("audit/logs.html", logs=logs)

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
