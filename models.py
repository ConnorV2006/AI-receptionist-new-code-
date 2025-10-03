from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------
# Roles
# -------------------------
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)


# -------------------------
# Users
# -------------------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    nurse_profile = db.relationship("NurseProfile", backref="user", uselist=False)
    receptionist_profile = db.relationship("ReceptionistProfile", backref="user", uselist=False)

    audit_logs = db.relationship("AuditLog", backref="user", lazy=True)


# -------------------------
# Patients
# -------------------------
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)

    appointments = db.relationship("Appointment", backref="patient", lazy=True)
    doctor_notes = db.relationship("DoctorNote", backref="patient", lazy=True)


# -------------------------
# Clinic
# -------------------------
class Clinic(db.Model):
    __tablename__ = "clinics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(50))
    twilio_token = db.Column(db.String(100))


# -------------------------
# Appointments
# -------------------------
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # link to doctor
    scheduled_time = db.Column(db.DateTime, nullable=False, index=True)


# -------------------------
# Doctor Notes
# -------------------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# -------------------------
# Nurse Profiles
# -------------------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nurse_id = db.Column(db.String(50), unique=True, nullable=False)


# -------------------------
# Receptionist Profiles
# -------------------------
class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receptionist_id = db.Column(db.String(50), unique=True, nullable=False)


# -------------------------
# Audit Logs
# -------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# -------------------------
# Fax Logs
# -------------------------
class FaxLog(db.Model):
    __tablename__ = "fax_logs"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # sent, received, failed, scheduled
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# -------------------------
# Twilio Logs (SMS, Calls, Faxes)
# -------------------------
class TwilioLog(db.Model):
    __tablename__ = "twilio_logs"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # "sms", "call", "fax"
    direction = db.Column(db.String(20), nullable=False)  # "inbound" / "outbound"
    from_number = db.Column(db.String(50), nullable=False)
    to_number = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False)  # sent, received, scheduled, failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
