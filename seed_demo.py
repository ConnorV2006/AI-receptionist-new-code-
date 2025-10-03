import os
from datetime import datetime, timedelta
from app import db, app
from models import (
    Role, User, Patient, Appointment, DoctorNote,
    NurseProfile, ReceptionistProfile, AuditLog, TwilioLog
)

def run_seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ----------------------------------------
        # Roles
        # ----------------------------------------
        roles = {}
        for role_name in ["Admin", "Doctor", "Nurse", "Receptionist", "Patient"]:
            role = Role(name=role_name)
            db.session.add(role)
            roles[role_name] = role
        db.session.commit()

        # ----------------------------------------
        # Users
        # ----------------------------------------
        admin = User(username="admin", email="admin@example.com", role=roles["Admin"])
        doctor = User(username="dr_smith", email="dr.smith@example.com", role=roles["Doctor"])
        nurse = User(username="nurse_jane", email="nurse.jane@example.com", role=roles["Nurse"])
        receptionist = User(username="reception_bob", email="bob@example.com", role=roles["Receptionist"])

        db.session.add_all([admin, doctor, nurse, receptionist])
        db.session.commit()

        # ----------------------------------------
        # Nurse & Receptionist Profiles
        # ----------------------------------------
        nurse_profile = NurseProfile(nurse_id=nurse.id, department="Cardiology")
        receptionist_profile = ReceptionistProfile(receptionist_id=receptionist.id, front_desk="Main Desk")
        db.session.add_all([nurse_profile, receptionist_profile])

        # ----------------------------------------
        # Patients
        # ----------------------------------------
        patients = [
            Patient(first_name="Alice", last_name="Brown", email="alice@example.com", phone="+123456789"),
            Patient(first_name="Bob", last_name="Jones", email="bob@example.com", phone="+198765432"),
            Patient(first_name="Carol", last_name="Taylor", email="carol@example.com", phone="+112233445"),
        ]
        db.session.add_all(patients)
        db.session.commit()

        # ----------------------------------------
        # Appointments (past, present, future)
        # ----------------------------------------
        now = datetime.utcnow()
        appointments = [
            Appointment(patient_id=patients[0].id, doctor_id=doctor.id, scheduled_time=now - timedelta(days=2)),
            Appointment(patient_id=patients[1].id, doctor_id=doctor.id, scheduled_time=now),
            Appointment(patient_id=patients[2].id, doctor_id=doctor.id, scheduled_time=now + timedelta(days=3)),
        ]
        db.session.add_all(appointments)
        db.session.commit()

        # ----------------------------------------
        # Doctor Notes
        # ----------------------------------------
        notes = [
            DoctorNote(doctor_id=doctor.id, patient_id=patients[0].id, content="Routine checkup - all good."),
            DoctorNote(doctor_id=doctor.id, patient_id=patients[1].id, content="Follow-up needed."),
        ]
        db.session.add_all(notes)

        # ----------------------------------------
        # Audit Logs
        # ----------------------------------------
        logs = [
            AuditLog(user_id=admin.id, action="Created system", details="Initial system setup"),
            AuditLog(user_id=doctor.id, action="Added note", details="Added patient note"),
            AuditLog(user_id=receptionist.id, action="Scheduled appointment", details="Bob Jones, tomorrow"),
        ]
        db.session.add_all(logs)

        # ----------------------------------------
        # Twilio Logs (SMS, Calls, Faxes)
        # ----------------------------------------
        twilio_logs = [
            # SMS
            TwilioLog(type="sms", from_number="+15550001", to_number="+123456789", content="Reminder: Appointment today", status="sent", timestamp=now),
            TwilioLog(type="sms", from_number="+123456789", to_number="+15550001", content="Thanks!", status="received", timestamp=now - timedelta(days=1)),

            # Call
            TwilioLog(type="call", from_number="+15550002", to_number="+198765432", content="Voicemail: Follow up needed", status="completed", timestamp=now - timedelta(days=2)),
            TwilioLog(type="call", from_number="+15550002", to_number="+198765432", content="Live call: patient spoke with nurse", status="answered", timestamp=now),

            # Fax
            TwilioLog(type="fax", from_number="+15550003", to_number="+112233445", content="Lab results", status="delivered", timestamp=now - timedelta(days=3)),
            TwilioLog(type="fax", from_number="+112233445", to_number="+15550003", content="Insurance paperwork", status="pending", timestamp=now + timedelta(days=1)),
        ]
        db.session.add_all(twilio_logs)

        db.session.commit()
        print("✅ Demo data seeded successfully!")

if __name__ == "__main__":
    run_seed()
