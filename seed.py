import os
from datetime import datetime, timedelta
from app import db
from models import (
    Role,
    User,
    Patient,
    Appointment,
    DoctorNote,
    NurseProfile,
    ReceptionistProfile,
    AuditLog,
    FaxLog,
    TwilioLog,
    Clinic,
)


def run_seed():
    print("🌱 Starting seed process...")

    # --- Roles ---
    roles = ["Admin", "Doctor", "Nurse", "Receptionist"]
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))
            print(f"✅ Role added: {role_name}")

    db.session.commit()

    # --- Users ---
    admin_role = Role.query.filter_by(name="Admin").first()
    doctor_role = Role.query.filter_by(name="Doctor").first()
    nurse_role = Role.query.filter_by(name="Nurse").first()
    receptionist_role = Role.query.filter_by(name="Receptionist").first()

    admin = User(username="admin", email="admin@example.com", password="hashedpassword", role_id=admin_role.id)
    doctor = User(username="dr_smith", email="drsmith@example.com", password="hashedpassword", role_id=doctor_role.id)
    nurse = User(username="nurse_jane", email="nursejane@example.com", password="hashedpassword", role_id=nurse_role.id)
    receptionist = User(username="reception_bob", email="receptionbob@example.com", password="hashedpassword", role_id=receptionist_role.id)

    for u in [admin, doctor, nurse, receptionist]:
        if not User.query.filter_by(email=u.email).first():
            db.session.add(u)
            print(f"✅ User added: {u.username}")

    db.session.commit()

    # --- Profiles ---
    nurse_user = User.query.filter_by(username="nurse_jane").first()
    if not NurseProfile.query.filter_by(user_id=nurse_user.id).first():
        db.session.add(NurseProfile(user_id=nurse_user.id, nurse_id="NURSE-1001"))
        print("✅ Nurse profile created")

    rec_user = User.query.filter_by(username="reception_bob").first()
    if not ReceptionistProfile.query.filter_by(user_id=rec_user.id).first():
        db.session.add(ReceptionistProfile(user_id=rec_user.id, receptionist_id="RECEP-2001"))
        print("✅ Receptionist profile created")

    db.session.commit()

    # --- Clinic ---
    if not Clinic.query.filter_by(slug="test").first():
        clinic = Clinic(
            name="Test Clinic",
            slug="test",
            twilio_number="+1234567890",
            twilio_sid="fakeSID",
            twilio_token="fakeTOKEN"
        )
        db.session.add(clinic)
        print("✅ Clinic created")
        db.session.commit()

    # --- Patients ---
    patient1 = Patient(first_name="John", last_name="Doe", email="john.doe@example.com", phone="555-111-2222")
    patient2 = Patient(first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone="555-333-4444")
    patient3 = Patient(first_name="Bob", last_name="Williams", email="bob.williams@example.com", phone="555-555-6666")

    for p in [patient1, patient2, patient3]:
        if not Patient.query.filter_by(email=p.email).first():
            db.session.add(p)
            print(f"✅ Patient added: {p.first_name} {p.last_name}")

    db.session.commit()

    # --- Appointments ---
    doctor = User.query.filter_by(username="dr_smith").first()
    patients = Patient.query.all()
    now = datetime.utcnow()

    appointments = [
        Appointment(patient_id=patients[0].id, doctor_id=doctor.id, scheduled_time=now - timedelta(days=2)),  # past
        Appointment(patient_id=patients[1].id, doctor_id=doctor.id, scheduled_time=now),  # present
        Appointment(patient_id=patients[2].id, doctor_id=doctor.id, scheduled_time=now + timedelta(days=2)),  # future
    ]

    for a in appointments:
        exists = Appointment.query.filter_by(patient_id=a.patient_id, doctor_id=a.doctor_id, scheduled_time=a.scheduled_time).first()
        if not exists:
            db.session.add(a)
            print(f"✅ Appointment scheduled for patient {a.patient_id}")

    db.session.commit()

    # --- Doctor Notes ---
    notes = [
        DoctorNote(patient_id=patients[0].id, doctor_id=doctor.id, content="Follow-up for blood pressure.", created_at=now - timedelta(days=2)),
        DoctorNote(patient_id=patients[1].id, doctor_id=doctor.id, content="Routine checkup today.", created_at=now),
        DoctorNote(patient_id=patients[2].id, doctor_id=doctor.id, content="Scheduled consultation in 2 days.", created_at=now + timedelta(days=2)),
    ]

    for n in notes:
        exists = DoctorNote.query.filter_by(patient_id=n.patient_id, doctor_id=n.doctor_id, content=n.content).first()
        if not exists:
            db.session.add(n)
            print(f"✅ Doctor note created for patient {n.patient_id}")

    db.session.commit()

    # --- Audit Logs ---
    audit_entries = [
        AuditLog(user_id=admin.id, action="User Login", details="Admin logged in", timestamp=now),
        AuditLog(user_id=doctor.id, action="Viewed Patient Record", details="Accessed John Doe", timestamp=now - timedelta(days=1)),
    ]
    for log in audit_entries:
        db.session.add(log)
    db.session.commit()
    print("✅ Audit logs added")

    # --- Fax Logs ---
    fax_entries = [
        FaxLog(sender="Clinic Fax", recipient="Insurance Office", status="sent", timestamp=now - timedelta(days=1)),
        FaxLog(sender="Lab", recipient="Clinic Fax", status="received", timestamp=now),
        FaxLog(sender="Clinic Fax", recipient="Specialist", status="scheduled", timestamp=now + timedelta(days=1)),
    ]
    for fax in fax_entries:
        db.session.add(fax)
    db.session.commit()
    print("✅ Fax logs added")

    # --- Twilio Logs ---
    twilio_entries = [
        # SMS
        TwilioLog(type="sms", direction="outbound", from_number="+1234567890", to_number=patients[0].phone, content="Reminder: Appointment tomorrow", status="sent", timestamp=now - timedelta(days=1)),
        TwilioLog(type="sms", direction="inbound", from_number=patients[1].phone, to_number="+1234567890", content="Confirming appointment today", status="received", timestamp=now),
        TwilioLog(type="sms", direction="outbound", from_number="+1234567890", to_number=patients[2].phone, content="Your appointment is scheduled in 2 days", status="scheduled", timestamp=now + timedelta(days=1)),

        # Calls
        TwilioLog(type="call", direction="outbound", from_number="+1234567890", to_number=patients[0].phone, content="Called patient for follow-up", status="completed", timestamp=now - timedelta(days=2)),
        TwilioLog(type="call", direction="inbound", from_number=patients[1].phone, to_number="+1234567890", content="Patient called to reschedule", status="completed", timestamp=now),

        # Fax
        TwilioLog(type="fax", direction="outbound", from_number="Clinic Fax", to_number="555-987-6543", content="Lab results faxed", status="sent", timestamp=now),
    ]

    for t in twilio_entries:
        db.session.add(t)
    db.session.commit()
    print("✅ Twilio logs added")

    print("🌱 Seed process complete!")


if __name__ == "__main__":
    run_seed()
