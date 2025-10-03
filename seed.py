from app import app, db
from models import Role, User, Clinic
from werkzeug.security import generate_password_hash


def run_seed():
    with app.app_context():
        # Seed roles
        roles = ["Admin", "SuperAdmin", "Receptionist", "Doctor", "Nurse"]
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))

        db.session.commit()

        # Seed default admin
        if not User.query.filter_by(username="admin").first():
            admin_role = Role.query.filter_by(name="Admin").first()
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("StrongP@ssw0rd!"),
                role_id=admin_role.id if admin_role else None,
            )
            db.session.add(admin_user)

        # Seed default clinic
        if not Clinic.query.filter_by(slug="test").first():
            clinic = Clinic(
                name="Test Clinic",
                slug="test",
                twilio_number="+12312448612"
            )
            db.session.add(clinic)

        db.session.commit()
        print("🌱 Database seeding completed successfully!")


if __name__ == "__main__":
    run_seed()
