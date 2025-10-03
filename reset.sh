#!/usr/bin/env bash
set -euo pipefail

echo "🚨 Resetting database for demo..."

# Drop all tables (force-clean demo environment)
psql "$DATABASE_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "📦 Running migrations..."
flask db upgrade

echo "🌱 Seeding demo data..."

python <<'EOF'
from app import db
from models import Role, User, Patient, Appointment, DoctorNote, AuditLog, NurseProfile, Clinic
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# --- Define FaxLog dynamically if not already in models ---
class FaxLog(db.Model):
    __tablename__ = "fax_logs"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # sent, received, failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure fax_logs table exists
db.create_all()

# --- Clear existing ---
db.session.query(Role).delete()
db.session.query(User).delete()
db.session.query(Patient).delete()
db.session.query(Appointment).delete()
db.session.query(DoctorNote).delete()
db.session.query(NurseProfile).delete()
db.session.query(AuditLog).delete()
db.session.query(FaxLog).delete()
db.session.commit()

# --- Roles ---
roles = {name: Role(name=name) for name in ["Admin", "Doctor", "Nurse", "Receptionist", "Patient"]}
db.session.add_all(roles.values())
db.session.commit()

# --- Users ---
admin = User(username="admin", email="admin@example.com", role=roles["Admin"])
doctor = User(username="dr_smith", email="dr.smith@example.com", role=roles["Doctor"])
nurse = User(username="nurse_amy", email="nurse.amy@example.com", role=roles["Nurse"])
receptionist = User(username="receptionist_john", email="reception.john@example.com", role=roles["Receptionist"])
patient_user = User(username="patient_jane", email="jane.doe@example.com", role=roles["Patient"])
db.session.add_all([admin, doctor, nurse, receptionist, patient_user])
db.session.commit()

# --- Profiles ---
clinic = Clinic(name="Demo Clinic", slug="demo-clinic")
db.session.add(clinic)
db.session.commit()

nurse_profile = NurseProfile(user_id=nurse.id, nurse_id="NURSE123")
db.session.add(nurse_profile)
db.session.commit()

# --- Patients ---
patient = Patient(first_name="Jane", last_name="Doe", email="jane.doe@example.com", phone="123-456-7890")
db.session.add(patient)
db.session.commit()

# --- Appointments ---
now = datetime.utcnow()
appointments = [
    Appointment(patient_id=patient.id, doctor_id=doctor.id, scheduled_time=now - timedelta(days=2)), # past
    Appointment(patient_id=patient.id, doctor_id=doctor.id, scheduled_time=now),                    # present
    Appointment(patient_id=patient.id, doctor_id=doctor.id, scheduled_time=now + timedelta(days=3)) # future
]
db.session.add_all(appointments)
db.session.commit()

# --- Doctor Notes ---
notes = [
    DoctorNote(patient_id=patient.id, doctor_id=doctor.id, content="Past checkup note", created_at=now - timedelta(days=2)),
    DoctorNote(patient_id=patient.id, doctor_id=doctor.id, content="Today's visit note", created_at=now),
    DoctorNote(patient_id=patient.id, doctor_id=doctor.id, content="Future scheduled note", created_at=now + timedelta(days=3))
]
db.session.add_all(notes)
db.session.commit()

# --- Twilio Samples ---
twilio_samples = [
    AuditLog(user_id=doctor.id, action="Twilio SMS sent", details="Reminder sent to patient", timestamp=now - timedelta(days=1)),
    AuditLog(user_id=patient_user.id, action="Twilio Call received", details="Patient called clinic", timestamp=now),
    AuditLog(user_id=receptionist.id, action="Twilio Call placed", details="Clinic called pharmacy", timestamp=now + timedelta(hours=3))
]
db.session.add_all(twilio_samples)
db.session.commit()

# --- Fax Logs (new table) ---
fax_samples = [
    FaxLog(sender="Clinic Fax +123456789", recipient="Lab Fax +198765432", status="sent", timestamp=now - timedelta(days=2)),
    FaxLog(sender="Hospital Fax +112233445", recipient="Clinic Fax +123456789", status="received", timestamp=now),
    FaxLog(sender="Clinic Fax +123456789", recipient="Insurance Fax +199988877", status="scheduled", timestamp=now + timedelta(days=1)),
]
db.session.add_all(fax_samples)
db.session.commit()

print("✅ Demo data (roles, users, patients, appointments, notes, SMS, calls, fax) seeded successfully!")
EOF

echo "🎉 Database reset + demo data seeded with SMS, Calls, Fax!"
