import os
from app import db, User, Role, Clinic

def run_seed():
    print("🌱 Running seed script...")

    # Seed roles
    for role_name in ["superadmin", "doctor", "nurse", "receptionist"]:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))
    db.session.commit()

    # Seed clinic
    clinic_slug = os.environ.get("INIT_CLINIC_SLUG", "test")
    if not Clinic.query.filter_by(slug=clinic_slug).first():
        clinic = Clinic(
            name=os.environ.get("INIT_CLINIC_NAME", "Test Clinic"),
            slug=clinic_slug
        )
        db.session.add(clinic)
        db.session.commit()

    # Seed superadmin user
    admin_username = os.environ.get("INIT_ADMIN_USERNAME", "admin")
    if not User.query.filter_by(username=admin_username).first():
        superadmin_role = Role.query.filter_by(name="superadmin").first()
        admin = User(
            username=admin_username,
            email=os.environ.get("INIT_ADMIN_EMAIL", "admin@example.com"),
            role_id=superadmin_role.id,
        )
        admin.set_password(os.environ.get("INIT_ADMIN_PASSWORD", "StrongP@ssw0rd!"))
        db.session.add(admin)
        db.session.commit()

    print("✅ Seeding complete!")

if __name__ == "__main__":
    run_seed()
