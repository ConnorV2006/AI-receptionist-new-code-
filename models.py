# models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ----------------------------
# Core Tables
# ----------------------------

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    audit_logs = db.relationship("AuditLog", backref="user", lazy=True)


class Clinic(db.Model):
    __tablename__ = "clinics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(120))
    twilio_token = db.Column(db.String(120))

    appointments = db.relationship("Appointment", backref="clinic", lazy=True)
    patients = db.relationship("Patient", backref="clinic", lazy=True)


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"))

    appointments = db.relationship("Appointment", backref="patient", lazy=True)
    doctor_notes = db.relationship("DoctorNote", backref="patient", lazy=True)


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    notes = db.relationship("DoctorNote", backref="appointment", lazy=True)


class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"
    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    specialization = db.Column(db.String(120))


class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"
    id = db.Column(db.Integer, primary_key=True)
    receptionist_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    desk_location = db.Column(db.String(120))


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ----------------------------
# Twilio Demo Logging
# ----------------------------

class TwilioLog(db.Model):
    __tablename__ = "twilio_logs"
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(20))  # SMS, CALL, FAX
    direction = db.Column(db.String(10))  # inbound / outbound
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=True)
