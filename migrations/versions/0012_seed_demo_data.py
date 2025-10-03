"""Seed demo patients, appointments, and doctor notes

Revision ID: 0012_seed_demo_data
Revises: 0011_add_doctor_time_composite
Create Date: 2025-10-03

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers, used by Alembic
revision = "0012_seed_demo_data"
down_revision = "0011_add_doctor_time_composite"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # --- Ensure roles exist ---
    roles = ["Admin", "Doctor", "Nurse", "Receptionist"]
    for role in roles:
        conn.execute(
            sa.text("INSERT INTO role (name) VALUES (:name) ON CONFLICT DO NOTHING"),
            {"name": role},
        )

    # --- Ensure admin user exists ---
    admin_email = "admin@example.com"
    admin_username = "admin"
    admin_password = "hashed_demo_password"  # <-- replace with hash if needed
    role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = 'Admin'")
    ).scalar()

    admin_user_id = conn.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": admin_email},
    ).scalar()

    if not admin_user_id and role_id:
        result = conn.execute(
            sa.text(
                """
                INSERT INTO users (username, email, password_hash, role_id, created_at)
                VALUES (:username, :email, :password_hash, :role_id, NOW())
                RETURNING id
                """
            ),
            {
                "username": admin_username,
                "email": admin_email,
                "password_hash": admin_password,
                "role_id": role_id,
            },
        )
        admin_user_id = result.scalar()

    # --- Seed demo clinic ---
    clinic_slug = "test"
    clinic_id = conn.execute(
        sa.text("SELECT id FROM clinic WHERE slug = :slug"),
        {"slug": clinic_slug},
    ).scalar()

    if not clinic_id:
        result = conn.execute(
            sa.text(
                """
                INSERT INTO clinic (name, slug, api_key, created_at)
                VALUES (:name, :slug, :api_key, NOW())
                RETURNING id
                """
            ),
            {
                "name": "Test Clinic",
                "slug": clinic_slug,
                "api_key": "some_default_key",
            },
        )
        clinic_id = result.scalar()

    # --- Seed demo patients ---
    demo_patients = [
        {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
    ]

    patient_ids = []
    for p in demo_patients:
        pid = conn.execute(
            sa.text("SELECT id FROM patients WHERE email = :email"),
            {"email": p["email"]},
        ).scalar()

        if not pid:
            result = conn.execute(
                sa.text(
                    """
                    INSERT INTO patients (first_name, last_name, email, created_at)
                    VALUES (:first_name, :last_name, :email, NOW())
                    RETURNING id
                    """
                ),
                p,
            )
            pid = result.scalar()
        patient_ids.append(pid)

    # --- Seed demo appointments + notes ---
    for i, pid in enumerate(patient_ids):
        scheduled_time = datetime.utcnow() + timedelta(days=i)

        appt_id = conn.execute(
            sa.text(
                """
                INSERT INTO appointments (patient_id, doctor_id, scheduled_time, reason)
                VALUES (:pid, :doctor_id, :scheduled_time, 'Routine checkup')
                RETURNING id
                """
            ),
            {"pid": pid, "doctor_id": admin_user_id, "scheduled_time": scheduled_time},
        ).scalar()

        conn.execute(
            sa.text(
                """
                INSERT INTO doctor_notes (patient_id, doctor_id, content, created_at)
                VALUES (:pid, :doctor_id, :content, NOW())
                """
            ),
            {
                "pid": pid,
                "doctor_id": admin_user_id,
                "content": f"Follow-up note for patient {pid}.",
            },
        )


def downgrade():
    # Rollback demo patients/appointments/notes only (safe cleanup)
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM doctor_notes WHERE content LIKE 'Follow-up note%'"))
    conn.execute(sa.text("DELETE FROM appointments WHERE reason = 'Routine checkup'"))
    conn.execute(sa.text("DELETE FROM patients WHERE email IN ('john@example.com','jane@example.com')"))
    conn.execute(sa.text("DELETE FROM clinic WHERE slug = 'test'"))
    conn.execute(sa.text("DELETE FROM users WHERE email = 'admin@example.com'"))
    # roles left intact since they may be used by real data
