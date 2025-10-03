from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ==========================
# Role
# ==========================
class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"


# ==========================
# User
# ==========================
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    role = db.relationship("Role", back_populates="users")
    patients = db.relationship("Patient", back_populates="doctor", lazy=True)
    appointments = db.relationship("Appointment", back_populates="doctor", lazy=True)
    audit_logs = db.relationship("AuditLog", back_populates="user", lazy=True)
    doctor_notes = db.relationship("DoctorNote", back_populates="doctor", lazy=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role.name})>"


# ==========================
# Patient
# ==========================
class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    doctor = db.relationship("User", back_populates="patients")

    appointments = db.relationship("Appointment", back_populates="patient", lazy=True)
    doctor_notes = db.relationship("DoctorNote", back_populates="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.name}>"


# ==========================
# Appointment
# ==========================
class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("User", back_populates="appointments")
    doctor_notes = db.relationship("DoctorNote", back_populates="appointment", lazy=True)

    def __repr__(self):
        return f"<Appointment {self.id} - {self.patient.name}>"


# ==========================
# Audit Log
# ==========================
class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} by {self.user.username}>"


# ==========================
# Clinic
# ==========================
class Clinic(db.Model):
    __tablename__ = "clinic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(255))
    twilio_token = db.Column(db.String(255))

    def __repr__(self):
        return f"<Clinic {self.name}>"


# ==========================
# Doctor Notes
# ==========================
class DoctorNote(db.Model):
    __tablename__ = "doctor_note"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))

    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = db.relationship("User", back_populates="doctor_notes")
    patient = db.relationship("Patient", back_populates="doctor_notes")
    appointment = db.relationship("Appointment", back_populates="doctor_notes")

    def __repr__(self):
        return f"<DoctorNote Doctor={self.doctor_id} Patient={self.patient_id}>"
