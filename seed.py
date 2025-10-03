import os
from datetime import datetime, timedelta

from app import db
from models import Role, User, Patient, Appointment, DoctorNote, AuditLog, NurseProfile

def run_seed():
    print("🌱 Seeding demo data...")

    db.drop_all()
    db.create_all()

    # -----------------------------
    # Roles
    # -----------------------------
    roles = {
        "Admin": Role(name="Admin"),
        "Doctor": Role(name="Doctor"),
        "Nurse": Role(name="Nurse"),
        "Receptionist": Role(name="Receptionist"),
    }
    db.session.add_all(roles.values())
    db.session.commit()

    # -----------------------------
    # Users
    # -----------------------------
    admin = User(username="admin", email="admin@example.com", password_hash="hash", role=roles["Admin"])
    doctor = User(username="drsmith", email="drsmith@example.com", password_hash="hash", role=roles["Doctor"])
    nurse = User(username="nursejane", email="nursejane@example.com", password_hash="hash", role=roles["Nurse"])
    receptionist = User(username="reception", email="reception@example.com", password_hash="hash", role=roles["Receptionist"])

    db.session.add_all([admin, doctor, nurse, receptionist])
    db.session.commit()

    # -----------------------------
    # Patients
    # -----------------------------
    john = Patient(first_name="John", last_name="Doe", email="john@example.com", phone="555-1234")
    jane = Patient(first_name="Jane", last_name="Smith", email="jane@example.com", phone="555-5678")
    carlos = Patient(first_name="Carlos", last_name="Martinez", email="carlos@example.com", phone="555-2468")

    db.session.add_all([john, jane, carlos])
    db.session.commit()

    # -----------------------------
    # Appointments
    # -----------------------------
    appts = [
        Appointment(patient=john, doctor=doctor, scheduled_time=datetime.utcnow() - timedelta(days=7), notes="Follow-up after surgery", status="completed"),
        Appointment(patient=jane, doctor=doctor, scheduled_time=datetime.utcnow() - timedelta(days=2), notes="Flu symptoms check", status="completed"),
        Appointment(patient=john, doctor=doctor, scheduled_time=datetime.utcnow(), notes="Annual check-up", status="scheduled"),
        Appointment(patient=jane, doctor=doctor, scheduled_time=datetime.utcnow(), notes="Follow-up visit", status="scheduled"),
        Appointment(patient=carlos, doctor=doctor, scheduled_time=datetime.utcnow(), notes="New patient intake", status="scheduled"),
        Appointment(patient=john, doctor=doctor, scheduled_time=datetime.utcnow() + timedelta(days=1), notes="Lab results discussion", status="scheduled"),
        Appointment(patient=jane, doctor=doctor, scheduled_time=datetime.utcnow() + timedelta(days=7), notes="1 week follow-up", status="scheduled"),
    ]
    db.session.add_all(appts)
    db.session.commit()

    # -----------------------------
    # Doctor Notes
    # -----------------------------
    notes = [
        DoctorNote(doctor=doctor, patient=john, content="Post-surgery recovery progressing well."),
        DoctorNote(doctor=doctor, patient=jane, content="Patient had flu, advised rest and hydration."),
        DoctorNote(doctor=doctor, patient=carlos, content="Initial consultation completed, labs pending."),
    ]
    db.session.add_all(notes)
    db.session.commit()

    # -----------------------------
    # Nurse + Reception Profiles
    # -----------------------------
    nurse_profile = NurseProfile(nurse_id=nurse.id, department="General Medicine")
    receptionist_profile = NurseProfile(nurse_id=receptionist.id, department="Front Desk / Reception")
    db.session.add_all([nurse_profile, receptionist_profile])
    db.session.commit()

    # -----------------------------
    # Audit Logs (Twilio samples: SMS, Calls, Fax)
    # -----------------------------
    logs = [
        # System
        AuditLog(user=admin, action="System initialized with base schema"),

        # Past
        AuditLog(user=doctor, action="Completed appointment for John Doe (7 days ago)"),
        AuditLog(user=doctor, action="Completed appointment for Jane Smith (2 days ago)"),
        AuditLog(user=receptionist, action="SMS sent via Twilio: 'Your appointment has been completed.' (2 days ago)"),
        AuditLog(user=receptionist, action="Inbound patient call missed (John Doe, 6 days ago)"),
        AuditLog(user=admin, action="Faxed lab results to Carlos Martinez (5 days ago)"),

        # Today
        AuditLog(user=receptionist, action="Checked in John Doe for annual check-up (today)"),
        AuditLog(user=nurse, action="Nurse Jane updated vitals for Carlos Martinez (today)"),
        AuditLog(user=receptionist, action="SMS reminder sent via Twilio: 'Your appointment is today at 3 PM.'"),
        AuditLog(user=doctor, action="Inbound call transferred to Dr. Smith via Twilio Voice (Jane Smith)"),
        AuditLog(user=receptionist, action="Fax confirmation received for lab order (today)"),

        # Future
        AuditLog(user=doctor, action="Scheduled follow-up for Jane Smith (in 7 days)"),
        AuditLog(user=doctor, action="Scheduled lab results discussion for John Doe (tomorrow)"),
        AuditLog(user=receptionist, action="Automated SMS scheduled: 'Reminder: Appointment tomorrow at 10 AM.'"),
        AuditLog(user=receptionist, action="Automated call scheduled to Jane Smith for appointment confirmation (in 3 days)"),
        AuditLog(user=admin, action="Fax queued for insurance paperwork submission (in 2 days)"),
    ]
    db.session.add_all(logs)
    db.session.commit()

    print("✅ Demo data seeded successfully.")


if __name__ == "__main__":
    run_seed()
