import time
from sqlalchemy import text
from app import db
from models import Role, User, Patient, Appointment, DoctorNote, NurseProfile, ReceptionistProfile, AuditLog, Clinic, TwilioLog


def wait_for_tables():
    """Wait until roles table is available."""
    for _ in range(5):
        try:
            db.session.execute(text("SELECT 1 FROM roles LIMIT 1;"))
            return True
        except Exception:
            time.sleep(2)
    return False


def run_seed():
    if not wait_for_tables():
        print("❌ Database tables not ready.")
        return

    # --- Roles ---
    role_names = ["Admin", "Doctor", "Nurse", "Receptionist"]
    roles = {}
    for role_name in role_names:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            print(f"✅ Added role: {role_name}")
        roles[role_name] = role
    db.session.commit()

    # --- Users ---
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password_hash="hashed_pw", role=roles["Admin"])
        db.session.add(admin)
        print("✅ Added admin user")

    doctor = User.query.filter_by(username="dr_smith").first()
    if not doctor:
        doctor = User(username="dr_smith", password_hash="hashed_pw", role=roles["Doctor"])
        db.session.add(doctor)
        print("✅ Added doctor user")

    nurse = User.query.filter_by(username="nurse_jane").first()
    if not nurse:
        nurse = User(username="nurse_jane", password_hash="hashed_pw", role=roles["Nurse"])
        db.session.add(nurse)
        print("✅ Added nurse user")

    receptionist = User.query.filter_by(username="reception_bob").first()
    if not receptionist:
        receptionist = User(username="reception_bob", password_hash="hashed_pw", role=roles["Receptionist"])
        db.session.add(receptionist)
        print("✅ Added receptionist user")

    db.session.commit()

    # --- Profiles ---
    if not NurseProfile.query.filter_by(nurse_id=nurse.id).first():
        db.session.add(NurseProfile(nurse_id=nurse.id, department="General Care"))
        print("✅ Added nurse profile")

    if not ReceptionistProfile.query.filter_by(receptionist_id=receptionist.id).first():
        db.session.add(ReceptionistProfile(receptionist_id=receptionist.id, desk_number="Front-1"))
        print("✅ Added receptionist profile")

    db.session.commit()

    # --- Clinic ---
    if not Clinic.query.filter_by(slug="test-clinic").first():
        db.session.add(Clinic(
            name="Test Clinic",
            slug="test-clinic",
            twilio_number="+1234567890",
            twilio_sid="SID123",
            twilio_token="TOKEN123"
        ))
        print("✅ Added demo clinic")
    db.session.commit()

    # --- Patients ---
    patients = []
    sample_patients = [
        ("John", "Doe", "john@example.com", "111-222-3333"),
        ("Mary", "Smith", "mary@example.com", "222-333-4444"),
        ("Alex", "Johnson", "alex@example.com", "333-444-5555"),
    ]
    for fname, lname, email, phone in sample_patients:
        p = Patient.query.filter_by(email=email).first()
        if not p:
            p = Patient(first_name=fname, last_name=lname, email=email, phone=phone)
            db.session.add(p)
            print(f"✅ Added patient: {fname} {lname}")
        patients.append(p)
    db.session.commit()

    # --- Appointments ---
    import datetime
    now = datetime.datetime.utcnow()
    appts = [
        Appointment(patient_id=patients[0].id, doctor_id=doctor.id, scheduled_time=now - datetime.timedelta(days=1), reason="Follow-up", status="completed"),
        Appointment(patient_id=patients[1].id, doctor_id=doctor.id, scheduled_time=now, reason="Consultation", status="scheduled"),
        Appointment(patient_id=patients[2].id, doctor_id=doctor.id, scheduled_time=now + datetime.timedelta(days=1), reason="Routine Check", status="scheduled"),
    ]
    for appt in appts:
        exists = Appointment.query.filter_by(patient_id=appt.patient_id, doctor_id=appt.doctor_id, scheduled_time=appt.scheduled_time).first()
        if not exists:
            db.session.add(appt)
    db.session.commit()
    print("✅ Added sample appointments")

    # --- Doctor Notes ---
    for p in patients:
        if not DoctorNote.query.filter_by(patient_id=p.id, doctor_id=doctor.id).first():
            db.session.add(DoctorNote(patient_id=p.id, doctor_id=doctor.id, note=f"Note for {p.first_name}"))
    db.session.commit()
    print("✅ Added doctor notes")

    # --- Audit Logs ---
    actions = ["Created appointment", "Updated patient info", "Logged in"]
    for action in actions:
        db.session.add(AuditLog(user_id=admin.id, action=action))
    db.session.commit()
    print("✅ Added audit logs")

    # --- Twilio Logs (SMS, Call, Fax) ---
    twilio_samples = [
        ("sms", "+1111111111", "+2222222222", "Past appointment reminder", "delivered"),
        ("sms", "+1111111111", "+2222222222", "Today’s appointment confirmed", "delivered"),
        ("sms", "+1111111111", "+2222222222", "Future follow-up scheduled", "queued"),
        ("call", "+3333333333", "+4444444444", "Inbound patient call", "completed"),
        ("fax", "+5555555555", "+6666666666", "Sent medical records", "sent"),
    ]
    for log_type, from_num, to_num, msg, status in twilio_samples:
        db.session.add(TwilioLog(
            log_type=log_type,
            from_number=from_num,
            to_number=to_num,
            message=msg,
            status=status
        ))
    db.session.commit()
    print("✅ Added Twilio logs")

    print("🌱 Database seeding complete.")


if __name__ == "__main__":
    run_seed()
