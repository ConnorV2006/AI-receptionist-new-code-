from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ----------------------------
# Role Model
# ----------------------------
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"


# ----------------------------
# User Model
# ----------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    audit_logs = db.relationship("AuditLog", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# ----------------------------
# Patient Model
# ----------------------------
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", backref="patient", lazy=True)
    notes = db.relationship("DoctorNote", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


# ----------------------------
# Appointment Model
# ----------------------------
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("User", foreign_keys=[doctor_id])

    def __repr__(self):
        return f"<Appointment Doctor={self.doctor_id} Patient={self.patient_id} At={self.scheduled_time}>"


# ----------------------------
# Doctor Notes
# ----------------------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("User", foreign_keys=[doctor_id])

    def __repr__(self):
        return f"<DoctorNote Doctor={self.doctor_id} Patient={self.patient_id}>"


# ----------------------------
# Nurse Profiles
# ----------------------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"

    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    department = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    nurse = db.relationship("User", foreign_keys=[nurse_id])

    def __repr__(self):
        return f"<NurseProfile Nurse={self.nurse_id}>"


# ----------------------------
# Audit Logs
# ----------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(256))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog User={self.user_id} Action={self.action}>"


# ----------------------------
# Twilio Logs (SMS, Call, Fax)
# ----------------------------
class TwilioLog(db.Model):
    __tablename__ = "twilio_logs"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # sms, call, fax
    from_number = db.Column(db.String(20), nullable=False)
    to_number = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TwilioLog {self.type.upper()} {self.from_number} -> {self.to_number} ({self.status})>"
