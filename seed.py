import os
from datetime import datetime, timedelta
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import inspect
from app import db
from models import Role, User, Clinic, Patient, Appointment, AuditLog, DoctorNote

def table_exists(table_name):
    """Check if a table exists in the DB before seeding."""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()

def run_seed():
    print("🔄 Starting database seeding...")

    # --- Seed Roles ---
    if table_exists("role"):
        for role_name in ["Admin", "Doctor", "Nurse", "Receptionist"]:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
                print(f"✅ Added role: {role_name}")
    else:
        print("⚠️ Skipping Role seeding (table not found).")

    # --- Seed Admin User ---
    admin_user = None
    if table_exists("users") and table_exists("role"):
        admin_email = os.environ.get("INIT_ADMIN_EMAIL", "admin@example.com")
        admin_username = os.environ.get("INIT_ADMIN_USERNAME", "admin")
        admin_password = os.environ.get("INIT_ADMIN_PASSWORD", "StrongP@ssw0rd!")
        admin_role = Role.query.filter_by(name="Admin").first()

        if admin_role and not User.query.filter_by(email=admin_email).first():
            admin_user = User(
                username=admin_username,
                email=admin_email,
                role_id=admin_role.id,
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            print("✅ Admin user created.")
        else:
            admin_user = User.query.filter_by(email=admin_email).first()
    else:
        print("⚠️ Skipping User seeding (table not found).")

    # --- Seed Clinic ---
    clinic = None
    if table_exists("clinic"):
        clinic_name = os.environ.get("INIT_CLINIC_NAME", "Test Clinic")
        clinic_slug = os.environ.get("INIT_CLINIC_SLUG", "test")
        api_key = os.environ.get("CLINIC_API_KEY_DEFAULT", "some_default_key")

        clinic = Clinic.query.filter_by(slug=clinic_slug).first()
        if not clinic:
            clinic = Clinic(
                name=clinic_name,
                slug=clinic_slug,
                api_key=api_key,
                created_at=datetime.utcnow(),
            )
            db.session.add(clinic)
            print(f"✅ Clinic '{clinic_name}' created.")
    else:
        print("⚠️ Skipping Clinic seeding (table not found).")

    # --- Seed Demo Patients ---
    patients = []
    if table_exists("patients"):
        demo_patients = [
            {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
        ]
        for pdata in demo_patients:
            existing = Patient.query.filter_by(email=pdata["email"]).first()
            if not existing:
                patient = Patient(
                    first_name=pdata["first_name"],
                    last_name=pdata["last_name"],
                    email=pdata["email"],
                    created_at=datetime.utcnow(),
                )
                db.session.add(patient)
                patients.append(patient)
                print(f"✅ Added patient: {pdata['first_name']} {pdata['last_name']}")
            else:
                patients.append(existing)
    else:
        print("⚠️ Skipping Patients seeding (table not found).")

    # --- Seed Demo Appointments ---
    appointments = []
    if table_exists("appointments") and patients and admin_user:
        for idx, patient in enumerate(patients):
            scheduled_time = datetime.utcnow() + timedelta(days=idx)
            appt = Appointment(
                patient_id=patient.id,
                doctor_id=admin_user.id,  # link to admin doctor for demo
                scheduled_time=scheduled_time,
                reason="Routine checkup",
            )
            db.session.add(appt)
            appointments.append(appt)
            print(f"✅ Added appointment for {patient.first_name} at {scheduled_time}")
    else:
        print("⚠️ Skipping Appointments seeding (tables or data missing).")

    # --- Seed Demo Doctor Notes ---
    if table_exists("doctor_notes") and appointments:
        for appt in appointments:
            note = DoctorNote(
                patient_id=appt.patient_id,
                doctor_id=appt.doctor_id,
                content=f"Follow-up note for patient {appt.patient_id}.",
                created_at=datetime.utcnow(),
            )
            db.session.add(note)
            print(f"✅ Added doctor note for patient {appt.patient_id}")
    else:
        print("⚠️ Skipping Doctor Notes seeding (table not found).")

    # --- Commit everything ---
    try:
        db.session.commit()
        print("🎉 Database seeding completed successfully!")
    except ProgrammingError as e:
        print(f"❌ Seeding failed: {e}")
        db.session.rollback()


if __name__ == "__main__":
    run_seed()
