import os
from app import app, db
from models import Role, User, Clinic
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import ProgrammingError, OperationalError
import time

def wait_for_tables():
    # simple probe to ensure at least one critical table exists
    for _ in range(10):
        try:
            db.session.execute("SELECT 1 FROM roles LIMIT 1;")
            return True
        except (ProgrammingError, OperationalError):
            print("⏳ Waiting for tables to be ready...")
            time.sleep(3)
    return False

def run_seed():
    with app.app_context():
        if not wait_for_tables():
            print("❌ Tables not ready; aborting seed.")
            return

        # Roles
        desired_roles = ["Admin", "Receptionist", "Doctor", "Nurse"]
        existing = {r.name for r in Role.query.all()}
        for name in desired_roles:
            if name not in existing:
                db.session.add(Role(name=name, description=f"Default {name} role"))
        db.session.commit()

        # Admin user
        if not User.query.filter_by(username=os.getenv("INIT_ADMIN_USERNAME", "admin")).first():
            admin_role = Role.query.filter_by(name="Admin").first()
            user = User(
                username=os.getenv("INIT_ADMIN_USERNAME", "admin"),
                email=os.getenv("INIT_ADMIN_EMAIL", "admin@example.com"),
                role_id=admin_role.id if admin_role else None,
            )
            user.password_hash = generate_password_hash(os.getenv("INIT_ADMIN_PASSWORD", "StrongP@ssw0rd!"))
            db.session.add(user)
            db.session.commit()

        # Clinic
        slug = os.getenv("INIT_CLINIC_SLUG", "test")
        if not Clinic.query.filter_by(slug=slug).first():
            db.session.add(Clinic(
                name=os.getenv("INIT_CLINIC_NAME", "Test Clinic"),
                slug=slug
            ))
            db.session.commit()

        print("🌱 Seeding complete.")

if __name__ == "__main__":
    run_seed()
