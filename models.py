from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# =========================================================
# Roles
# =========================================================
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"


# =========================================================
# Users
# =========================================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship(
        "Appointment", backref="doctor", lazy=True, foreign_keys="Appointment.doctor_id"
    )
    notes = db.relationship(
        "DoctorNote", backref="doctor", lazy=True, foreign_keys="DoctorNote.doctor_id"
    )
    audit_logs = db.relationship("AuditLog", backref="user", lazy=True)
    nurse_profile = db.relationship("NurseProfile", backref="nurse", uselist=False)
    receptionist_profile = db.relationship("ReceptionistProfile", backref="receptionist", uselist=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role.name if self.role else 'No Role'})>"


# =========================================================
# Patients
# =========================================================
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


# =========================================================
# Appointments
# =========================================================
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Appointment Doctor={self.doctor_id} Patient={self.patient_id} at {self.scheduled_time}>"


# =========================================================
# Doctor Notes
# =========================================================
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DoctorNote Doctor={self.doctor_id} Patient={self.patient_id}>"


# =========================================================
# Nurse Profiles
# =========================================================
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"

    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    department = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NurseProfile Nurse={self.nurse_id} Department={self.department}>"


# =========================================================
# Receptionist Profiles
# =========================================================
class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"

    id = db.Column(db.Integer, primary_key=True)
    receptionist_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    front_desk = db.Column(db.String(120))  # e.g., "Main Desk", "ER Desk"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ReceptionistProfile Receptionist={self.receptionist_id} Desk={self.front_desk}>"


# =========================================================
# Audit Logs
# =========================================================
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(256))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog User={self.user_id} Action={self.action}>"


# =========================================================
# Twilio Logs (SMS, Calls, Faxes)
# =========================================================
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
        return f"<TwilioLog {self.type.upper()} from {self.from_number} to {self.to_number}>"
