import os
from io import BytesIO
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from functools import wraps

# -------------------------------------------------
# App + Config
# -------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from models import User, Clinic, Patient, Visit, Paystub, Appointment, Reminder, FileUpload, CallLog, MessageLog

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------
# Role-based access decorator
# -------------------------------------------------
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if "role" not in session:
                flash("You must log in first.")
                return redirect(url_for("login"))
            if session["role"] != role and session["role"] != "superadmin":
                flash("Access denied: insufficient permissions.")
                return redirect(url_for("dashboard"))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# -------------------------------------------------
# Auth Routes
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        flash("You must log in first.")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if request.method == "POST":
        old_pw = request.form["old_password"]
        new_pw = request.form["new_password"]
        confirm_pw = request.form["confirm_password"]

        if not user.check_password(old_pw):
            flash("Old password is incorrect.")
            return redirect(url_for("change_password"))

        if new_pw != confirm_pw:
            flash("New passwords do not match.")
            return redirect(url_for("change_password"))

        user.set_password(new_pw)
        db.session.commit()
        flash("Password updated successfully.")
        return redirect(url_for("dashboard"))

    return render_template("change_password.html")

# -------------------------------------------------
# Dashboard
# -------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# -------------------------------------------------
# Users (superadmin only)
# -------------------------------------------------
@app.route("/users", methods=["GET", "POST"])
@role_required("superadmin")
def manage_users():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        new_user = User(email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("New user created successfully!")
        return redirect(url_for("manage_users"))

    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/promote/<int:user_id>/<string:new_role>")
@role_required("superadmin")
def promote_user(user_id, new_role):
    user = User.query.get_or_404(user_id)
    if user.role == "superadmin":
        flash("You cannot change another superadmin.")
        return redirect(url_for("manage_users"))
    user.role = new_role
    db.session.commit()
    flash(f"{user.email} updated to {new_role}")
    return redirect(url_for("manage_users"))

@app.route("/users/delete/<int:user_id>")
@role_required("superadmin")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == "superadmin":
        flash("You cannot delete a superadmin.")
        return redirect(url_for("manage_users"))
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully")
    return redirect(url_for("manage_users"))

# -------------------------------------------------
# Paystubs, Appointments, Reminders, Visits, Logs...
# (unchanged from previous version)
# -------------------------------------------------
# ... keep all the same routes we already built for paystubs, appointments, reminders, visits, audit-logs, quick replies ...
