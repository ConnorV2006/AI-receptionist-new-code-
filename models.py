import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db

# -------------------------------------------------
# Role model
# -------------------------------------------------
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="role", lazy=True)


# -------------------------------------------------
# User model
# -------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", back_populates="users")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship("Appointment", back_populates="doctor", lazy=True)
    notes = db.relationship("DoctorNote", back_populates="doctor", lazy=True)
    nurse_profile = db.relationship("NurseProfile", uselist=False, back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------------------------------------
# Clinic model
# -------------------------------------------------
class Clinic(db.Model):
    __tablename__ = "clinic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", back_populates="clinic", lazy=True)
    patients = db.relationship("Patient", back_populates="clinic", lazy=True)


# -------------------------------------------------
# Patient model
# -------------------------------------------------
class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    clinic = db.relationship("Clinic", back_populates="patients")

    appointments = db.relationship("Appointment", back_populates="patient", lazy=True)
    notes = db.relationship("DoctorNote", back_populates="patient", lazy=True)


# -------------------------------------------------
# Appointment model
# -------------------------------------------------
class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("User", back_populates="appointments")
    clinic = db.relationship("Clinic", back_populates="appointments")

    notes = db.relationship("DoctorNote", back_populates="appointment", lazy=True)


# -------------------------------------------------
# Doctor Notes model
# -------------------------------------------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_note"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))

    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = db.relationship("User", back_populates="notes")
    patient = db.relationship("Patient", back_populates="notes")
    appointment = db.relationship("Appointment", back_populates="notes")


# -------------------------------------------------
# Nurse Profile model
# -------------------------------------------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=True)
    shift = db.Column(db.String(50), nullable=True)

    user = db.relationship("User", back_populates="nurse_profile")


# -------------------------------------------------
# Audit Log model
# -------------------------------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
