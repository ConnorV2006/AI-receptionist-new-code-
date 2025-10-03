from datetime import datetime, timedelta
from models import db, Role, User, Patient, Appointment, DoctorNote, NurseProfile, AuditLog, TwilioLog

def run_demo_seed():
    """Seed demo data for showcasing the system to businesses."""

    # --- Roles ---
    roles = ["Admin", "Doctor", "Nurse", "Receptionist"]
    for r in roles:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r))

    db.session.commit()

    # --- Users ---
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", email="admin@example.com", role=Role.query.filter_by(name="Admin").first())
        admin.set_password("StrongP@ssw0rd!")
        db.session.add(admin)

    doctor = User.query.filter_by(username="dr_smith").first()
    if not doctor:
        doctor = User(username="dr_smith", email="drsmith@example.com", role=Role.query.filter_by(name="Doctor").first())
        doctor.set_password("doctorpass")
        db.session.add(doctor)

    nurse = User.query.filter_by(username="nurse_jane").first()
    if not nurse:
        nurse = User(username="nurse_jane", email="nursejane@example.com", role=Role.query.filter_by(name="Nurse").first())
        nurse.set_password("nursepass")
        db.session.add(nurse)

    receptionist = User.query.filter_by(username="receptionist_kate").first()
    if not receptionist:
        receptionist = User(username="receptionist_kate", email="kate@example.com", role=Role.query.filter_by(name="Receptionist").first())
        receptionist.set_password("receptionpass")
        db.session.add(receptionist)

    db.session.commit()

    # --- Nurse Profile ---
    if not NurseProfile.query.filter_by(nurse_id=nurse.id).first():
        nurse_profile = NurseProfile(nurse_id=nurse.id, department="General Care")
        db.session.add(nurse_profile)
        db.session.commit()

    # --- Patients ---
    patient1 = Patient.query.filter_by(email="john.doe@example.com").first()
    if not patient1:
        patient1 = Patient(first_name="John", last_name="Doe", email="john.doe@example.com", phone="+1234567890")
        db.session.add(patient1)

    patient2 = Patient.query.filter_by(email="jane.smith@example.com").first()
    if not patient2:
        patient2 = Patient(first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone="+1987654321")
        db.session.add(patient2)

    db.session.commit()

    # --- Appointments (Past, Present, Future) ---
    appts = [
        Appointment(patient_id=patient1.id, doctor_id=doctor.id, scheduled_time=datetime.utcnow() - timedelta(days=2)),
        Appointment(patient_id=patient2.id, doctor_id=doctor.id, scheduled_time=datetime.utcnow()),  # today
        Appointment(patient_id=patient1.id, doctor_id=doctor.id, scheduled_time=datetime.utcnow() + timedelta(days=3)),
    ]
    for a in appts:
        if not Appointment.query.filter_by(patient_id=a.patient_id, doctor_id=a.doctor_id, scheduled_time=a.scheduled_time).first():
            db.session.add(a)

    db.session.commit()

    # --- Doctor Notes ---
    note = DoctorNote.query.first()
    if not note:
        db.session.add(DoctorNote(doctor_id=doctor.id, patient_id=patient1.id, content="Patient recovering well. Prescribed rest."))
        db.session.add(DoctorNote(doctor_id=doctor.id, patient_id=patient2.id, content="Patient experiencing mild symptoms. Follow-up in 1 week."))
        db.session.commit()

    # --- Audit Logs ---
    logs = [
        AuditLog(user_id=admin.id, action="Created demo system", details="Initial demo setup"),
        AuditLog(user_id=doctor.id, action="Checked patient record", details="Accessed John Doe record"),
        AuditLog(user_id=receptionist.id, action="Scheduled appointment", details="Appointment for Jane Smith"),
    ]
    for log in logs:
        db.session.add(log)

    db.session.commit()

    # --- Twilio Logs (SMS, Call, Fax) ---
    sms = TwilioLog.query.filter_by(type="sms").first()
    if not sms:
        db.session.add(TwilioLog(
            type="sms",
            from_number="+12312448612",
            to_number=patient1.phone,
            content="Reminder: Your appointment is tomorrow at 10 AM.",
            status="delivered",
            timestamp=datetime.utcnow() - timedelta(hours=1)
        ))

    call = TwilioLog.query.filter_by(type="call").first()
    if not call:
        db.session.add(TwilioLog(
            type="call",
            from_number="+12312448612",
            to_number=patient2.phone,
            content="Call placed to confirm appointment.",
            status="completed",
            timestamp=datetime.utcnow()
        ))

    fax = TwilioLog.query.filter_by(type="fax").first()
    if not fax:
        db.session.add(TwilioLog(
            type="fax",
            from_number="+12312448612",
            to_number="+11234567890",
            content="Fax sent with lab results.",
            status="sent",
            timestamp=datetime.utcnow() - timedelta(days=1)
        ))

    db.session.commit()
    print("🌱 Demo data seeded successfully!")
