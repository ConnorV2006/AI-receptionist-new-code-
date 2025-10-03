from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# -------------------
# Role Table
# -------------------
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)


# -------------------
# User Table
# -------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clinics = db.relationship("Clinic", backref="owner", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------
# Clinic Table
# -------------------
class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------
# Patient Table
# -------------------
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------
# Appointment Table
# -------------------
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="appointments")
    doctor = db.relationship("User", backref="appointments")


# -------------------
# Notes (Doctor Notes)
# -------------------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("User", backref="notes")
    patient = db.relationship("Patient", backref="notes")


# -------------------
# Call Logs
# -------------------
class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    status = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------
# Message Logs
# -------------------
class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------
# Audit Logs
# -------------------
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")
