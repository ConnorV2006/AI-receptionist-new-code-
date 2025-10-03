import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# -------------------------
# Roles
# -------------------------
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"


# -------------------------
# Users
# -------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship("Role", back_populates="users")
    nurse_profile = db.relationship("NurseProfile", back_populates="user", uselist=False)
    receptionist_profile = db.relationship("ReceptionistProfile", back_populates="user", uselist=False)

    appointments = db.relationship("Appointment", back_populates="doctor", lazy=True, foreign_keys="Appointment.doctor_id")
    doctor_notes = db.relationship("DoctorNote", back_populates="doctor", lazy=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role.name if self.role else 'No Role'})>"


# -------------------------
# Patients
# -------------------------
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", back_populates="patient", lazy=True)
    doctor_notes = db.relationship("DoctorNote", back_populates="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


# -------------------------
# Appointments
# -------------------------
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    scheduled_time = db.Column(db.DateTime, nullable=False, index=True)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("User", back_populates="appointments")

    __table_args__ = (
        db.Index("ix_appointments_doctor_time", "doctor_id", "scheduled_time"),
    )

    def __repr__(self):
        return f"<Appointment Doctor={self.doctor_id} Patient={self.patient_id} at {self.scheduled_time}>"


# -------------------------
# Doctor Notes
# -------------------------
class DoctorNote(db.Model):
    __tablename__ = "doctor_notes"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    patient = db.relationship("Patient", back_populates="doctor_notes")
    doctor = db.relationship("User", back_populates="doctor_notes")

    def __repr__(self):
        return f"<DoctorNote Doctor={self.doctor_id} Patient={self.patient_id}>"


# -------------------------
# Audit Logs
# -------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AuditLog {self.user_id} {self.action}>"


# -------------------------
# Nurse Profile
# -------------------------
class NurseProfile(db.Model):
    __tablename__ = "nurse_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    nurse_id = db.Column(db.String(50), unique=True, nullable=False)

    user = db.relationship("User", back_populates="nurse_profile")

    def __repr__(self):
        return f"<NurseProfile {self.nurse_id}>"


# -------------------------
# Receptionist Profile
# -------------------------
class ReceptionistProfile(db.Model):
    __tablename__ = "receptionist_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    receptionist_id = db.Column(db.String(50), unique=True, nullable=False)

    user = db.relationship("User", back_populates="receptionist_profile")

    def __repr__(self):
        return f"<ReceptionistProfile {self.receptionist_id}>"


# -------------------------
# Twilio Logs
# -------------------------
class TwilioLog(db.Model):
    __tablename__ = "twilio_logs"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # sms, call, fax
    direction = db.Column(db.String(20), nullable=False)  # inbound, outbound
    from_number = db.Column(db.String(20), nullable=False)
    to_number = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<TwilioLog {self.type.upper()} {self.direction} {self.status}>"


# -------------------------
# Clinic
# -------------------------
class Clinic(db.Model):
    __tablename__ = "clinics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(100))
    twilio_token = db.Column(db.String(100))

    def __repr__(self):
        return f"<Clinic {self.name}>"
