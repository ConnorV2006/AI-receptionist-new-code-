from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# --------------------------
# Role Model
# --------------------------
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


# --------------------------
# User Model
# --------------------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship("Role", backref="users")

    def __repr__(self):
        return f"<User {self.username}>"


# --------------------------
# Patient Model
# --------------------------
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)

    appointments = db.relationship("Appointment", backref="patient", cascade="all, delete-orphan")
    notes = db.relationship("DoctorNote", backref="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


# --------------------------
# Appointment Model
# --------------------------
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))

    def __repr__(self):
        return f"<Appointment Doctor {self.doctor_id} @ {self.scheduled_time}>"


# --------------------------
# Doctor Notes
# --------------------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DoctorNote Doctor {self.doctor_id} Patient {self.patient_id}>"


# --------------------------
# Nurse Profiles
# --------------------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    nurse_id = db.Column(db.String(50), unique=True)

    user = db.relationship("User", backref="nurse_profile")

    def __repr__(self):
        return f"<NurseProfile {self.nurse_id}>"


# --------------------------
# Receptionist Profiles
# --------------------------
class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    receptionist_id = db.Column(db.String(50), unique=True)

    user = db.relationship("User", backref="receptionist_profile")

    def __repr__(self):
        return f"<ReceptionistProfile {self.receptionist_id}>"


# --------------------------
# Audit Logs
# --------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} by User {self.user_id}>"


# --------------------------
# Twilio Logs (SMS, Calls, Fax)
# --------------------------
class TwilioLog(db.Model):
    __tablename__ = "twilio_logs"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # sms, call, fax
    direction = db.Column(db.String(20), nullable=False)  # inbound/outbound
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    content = db.Column(db.Text)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TwilioLog {self.type} {self.direction} {self.status}>"
