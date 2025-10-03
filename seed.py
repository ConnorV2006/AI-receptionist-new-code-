from datetime import datetime, timedelta
from app import db
from models import (
    Role, User, Patient, Appointment, DoctorNote,
    NurseProfile, ReceptionistProfile, AuditLog,
    Clinic, FaxLog, TwilioLog
)

def run_seed():
    print("🌱 Starting seed...")

    # Reset DB (for demo purposes)
    db.drop_all()
    db.create_all()

    # ------------------------
    # Roles
    # ------------------------
    roles = {
        "Admin": Role(name="Admin"),
        "Doctor": Role(name="Doctor"),
        "Nurse": Role(name="Nurse"),
        "Receptionist": Role(name="Receptionist")
    }
    db.session.add_all(roles.values())
    db.session.commit()

    # ------------------------
    # Users
    # ------------------------
    admin = User(username="admin1", email="admin@example.com", password="hashed_pw", role=roles["Admin"])
    doctor = User(username="dr_smith", email="dr.smith@example.com", password="hashed_pw", role=roles["Doctor"])
    nurse = User(username="nurse_amy", email="nurse.amy@example.com", password="hashed_pw", role=roles["Nurse"])
    receptionist = User(username="reception_john", email="reception.john@example.com", password="hashed_pw", role=roles["Receptionist"])

    db.session.add_all([admin, doctor, nurse, receptionist])
    db.session.commit()

    # ------------------------
    # Patients
    # ------------------------
    patient1 = Patient(first_name="Alice", last_name="Johnson", email="alice.johnson@example.com", phone="555-1111")
    patient2 = Patient(first_name="Bob", last_name="Williams", email="bob.williams@example.com", phone="555-2222")
    patient3 = Patient(first_name="Carol", last_name="Brown", email="carol.brown@example.com", phone="555-3333")
    db.session.add_all([patient1, patient2, patient3])
    db.session.commit()

    # ------------------------
    # Clinic
    # ------------------------
    clinic = Clinic(
        name="Downtown Health Clinic",
        slug="downtown-health",
        twilio_number="+15551234567",
        twilio_sid="ACXXXXXXXXXXXXXXXX",
        twilio_token="your_twilio_auth_token"
    )
    db.session.add(clinic)
    db.session.commit()

    # ------------------------
    # Appointments
    # ------------------------
    now = datetime.utcnow()
    appointments = [
        Appointment(patient_id=patient1.id, doctor_id=doctor.id, scheduled_time=now - timedelta(days=2)),  # past
        Appointment(patient_id=patient2.id, doctor_id=doctor.id, scheduled_time=now),  # present
        Appointment(patient_id=patient3.id, doctor_id=doctor.id, scheduled_time=now + timedelta(days=3)),  # future
    ]
    db.session.add_all(appointments)
    db.session.commit()

    # ------------------------
    # Doctor Notes
    # ------------------------
    notes = [
        DoctorNote(patient_id=patient1.id, doctor_id=doctor.id, content="Follow-up after flu symptoms.", created_at=now - timedelta(days=2)),
        DoctorNote(patient_id=patient2.id, doctor_id=doctor.id, content="Routine check-up, all good.", created_at=now),
        DoctorNote(patient_id=patient3.id, doctor_id=doctor.id, content="Upcoming consultation for back pain.", created_at=now + timedelta(days=1)),
    ]
    db.session.add_all(notes)
    db.session.commit()

    # ------------------------
    # Nurse & Receptionist Profiles
    # ------------------------
    nurse_profile = NurseProfile(user_id=nurse.id, nurse_id="NURSE001")
    receptionist_profile = ReceptionistProfile(user_id=receptionist.id, receptionist_id="RECEP001")
    db.session.add_all([nurse_profile, receptionist_profile])
    db.session.commit()

    # ------------------------
    # Audit Logs
    # ------------------------
    logs = [
        AuditLog(user_id=admin.id, action="Created User", details="Added Dr. Smith as a doctor.", timestamp=now - timedelta(days=5)),
        AuditLog(user_id=doctor.id, action="Updated Appointment", details="Rescheduled Alice's appointment.", timestamp=now - timedelta(days=1)),
        AuditLog(user_id=receptionist.id, action="Checked-In Patient", details="Bob checked in at reception.", timestamp=now),
    ]
    db.session.add_all(logs)
    db.session.commit()

    # ------------------------
    # Fax Logs
    # ------------------------
    faxes = [
        FaxLog(sender="clinic@example.com", recipient="lab@example.com", status="sent", timestamp=now - timedelta(days=2)),
        FaxLog(sender="lab@example.com", recipient="clinic@example.com", status="received", timestamp=now - timedelta(days=1)),
        FaxLog(sender="clinic@example.com", recipient="pharmacy@example.com", status="scheduled", timestamp=now + timedelta(hours=2)),
        FaxLog(sender="clinic@example.com", recipient="insurance@example.com", status="failed", timestamp=now - timedelta(hours=5)),
    ]
    db.session.add_all(faxes)
    db.session.commit()

    # ------------------------
    # Twilio Logs (SMS + Calls + Fax references)
    # ------------------------
    twilio_logs = [
        # SMS examples
        TwilioLog(type="sms", direction="inbound", from_number="+15554443333", to_number=clinic.twilio_number, content="Hi, I need to schedule an appointment.", status="received", timestamp=now - timedelta(days=1)),
        TwilioLog(type="sms", direction="outbound", from_number=clinic.twilio_number, to_number="+15554443333", content="Your appointment is confirmed for tomorrow at 10am.", status="sent", timestamp=now),
        TwilioLog(type="sms", direction="outbound", from_number=clinic.twilio_number, to_number="+15554443333", content="Reminder: Appointment tomorrow!", status="scheduled", timestamp=now + timedelta(hours=12)),

        # Call examples
        TwilioLog(type="call", direction="inbound", from_number="+15556667777", to_number=clinic.twilio_number, content="Patient called for test results.", status="completed", timestamp=now - timedelta(days=2)),
        TwilioLog(type="call", direction="outbound", from_number=clinic.twilio_number, to_number="+15556667777", content="Clinic follow-up call placed.", status="in-progress", timestamp=now),
        TwilioLog(type="call", direction="outbound", from_number=clinic.twilio_number, to_number="+15556667777", content="Future call scheduled.", status="scheduled", timestamp=now + timedelta(days=1)),

        # Fax references (linking to FaxLog if you want cross-reference)
        TwilioLog(type="fax", direction="outbound", from_number="clinic@example.com", to_number="lab@example.com", content="Lab results faxed.", status="sent", timestamp=now - timedelta(days=2)),
    ]
    db.session.add_all(twilio_logs)
    db.session.commit()

    print("✅ Seeding complete! Demo data is ready with SMS, Calls, and Faxes.")


if __name__ == "__main__":
    run_seed()
