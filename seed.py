import os
from datetime import datetime
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import inspect
from app import db
from models import Role, User, Clinic, Patient, Appointment, AuditLog

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
                role = Role(name=role_name)
                db.session.add(role)
                print(f"✅ Added role: {role_name}")
    else:
        print("⚠️ Skipping Role seeding (table not found).")

    # --- Seed Admin User ---
    if table_exists("users") and table_exists("role"):
        admin_email = os.environ.get("INIT_ADMIN_EMAIL", "admin@example.com")
        admin_username = os.environ.get("INIT_ADMIN_USERNAME", "admin")
        admin_password = os.environ.get("INIT_ADMIN_PASSWORD", "StrongP@ssw0rd!")
        admin_role = Role.query.filter_by(name="Admin").first()

        if admin_role and not User.query.filter_by(email=admin_email).first():
            admin = User(
                username=admin_username,
                email=admin_email,
                role_id=admin_role.id,
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            print("✅ Admin user created.")
    else:
        print("⚠️ Skipping User seeding (table not found).")

    # --- Seed Clinic ---
    if table_exists("clinic"):
        clinic_name = os.environ.get("INIT_CLINIC_NAME", "Test Clinic")
        clinic_slug = os.environ.get("INIT_CLINIC_SLUG", "test")
        api_key = os.environ.get("CLINIC_API_KEY_DEFAULT", "some_default_key")

        if not Clinic.query.filter_by(slug=clinic_slug).first():
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

    # --- Commit everything ---
    try:
        db.session.commit()
        print("🎉 Database seeding completed successfully!")
    except ProgrammingError as e:
        print(f"❌ Seeding failed: {e}")
        db.session.rollback()


if __name__ == "__main__":
    run_seed()
