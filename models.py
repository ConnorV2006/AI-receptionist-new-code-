from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# -----------------
# Roles
# -----------------
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# -----------------
# Users
# -----------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", backref=db.backref("users", lazy=True))


# -----------------
# Patients
# -----------------
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -----------------
# Appointments
# -----------------
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)

    patient = db.relationship("Patient", backref=db.backref("appointments", lazy=True))
    doctor = db.relationship("User", backref=db.backref("appointments", lazy=True))


# -----------------
# Doctor Notes
# -----------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref=db.backref("doctor_notes", lazy=True))
    doctor = db.relationship("User", backref=db.backref("doctor_notes", lazy=True))


# -----------------
# Nurse Profiles
# -----------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nurse_id = db.Column(db.String(50), unique=True, nullable=False)

    user = db.relationship("User", backref=db.backref("nurse_profile", uselist=False))


# -----------------
# Receptionist Profiles
# -----------------
class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receptionist_id = db.Column(db.String(50), unique=True, nullable=False)

    user = db.relationship("User", backref=db.backref("receptionist_profile", uselist=False))


# -----------------
# Audit Logs
# -----------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("audit_logs", lazy=True))


# -----------------
# Clinic
# -----------------
class Clinic(db.Model):
    __tablename__ = "clinics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(120))
    twilio_token = db.Column(db.String(120))


# -----------------
# Fax Logs
# -----------------
class FaxLog(db.Model):
    __tablename__ = "fax_logs"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # sent, received, failed, scheduled
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<FaxLog {self.sender} -> {self.recipient} ({self.status})>"
