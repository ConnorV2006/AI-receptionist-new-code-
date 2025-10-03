from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

# -------------------------
# USER
# -------------------------
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="receptionist")  
    # roles: receptionist, nurse, doctor, admin, superadmin

    # One-to-one optional link to Nurse profile
    nurse_profile = db.relationship("Nurse", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"


# -------------------------
# NURSE PROFILE
# -------------------------
class Nurse(db.Model):
    __tablename__ = "nurse"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    specialty = db.Column(db.String(120))
    shift = db.Column(db.String(50))
    license_number = db.Column(db.String(50))

    def __repr__(self):
        return f"<Nurse user_id={self.user_id}, specialty={self.specialty}, shift={self.shift}>"


# -------------------------
# PATIENT
# -------------------------
class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", backref="patient", lazy=True)


# -------------------------
# APPOINTMENT
# -------------------------
class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------
# AUDIT LOG
# -------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))  # could be user_id in future
    action = db.Column(db.String(255))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
