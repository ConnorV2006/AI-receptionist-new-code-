"""Seed demo doctor note and nurse profile

Revision ID: 0009_seed_notes
Revises: 0008_add_notes_profiles
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# Revision identifiers, used by Alembic.
revision = "0009_seed_notes"
down_revision = "0008_add_notes_profiles"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # --- Look up dr_smith (doctor) and nurse_anna (nurse) ---
    doctor_user_id = conn.execute(
        sa.text("SELECT id FROM users WHERE username = 'dr_smith'")
    ).scalar()

    doctor_id = None
    if doctor_user_id:
        doctor_id = conn.execute(
            sa.text("SELECT id FROM doctors WHERE user_id = :uid"),
            {"uid": doctor_user_id},
        ).scalar()

    nurse_user_id = conn.execute(
        sa.text("SELECT id FROM users WHERE username = 'nurse_anna'")
    ).scalar()

    nurse_id = None
    if nurse_user_id:
        nurse_id = conn.execute(
            sa.text("SELECT id FROM nurses WHERE user_id = :uid"),
            {"uid": nurse_user_id},
        ).scalar()

    # --- Ensure a demo patient exists ---
    patient_id = conn.execute(
        sa.text("SELECT id FROM patients WHERE email = 'john.doe@example.com'")
    ).scalar()

    if not patient_id:
        conn.execute(
            sa.text(
                """
                INSERT INTO patients (first_name, last_name, dob, phone, email, clinic_id)
                VALUES (:fn, :ln, :dob, :phone, :email, 
                        (SELECT id FROM clinics WHERE slug = 'test' LIMIT 1))
                """
            ),
            {
                "fn": "John",
                "ln": "Doe",
                "dob": datetime(1990, 1, 1).date(),
                "phone": "+15555550123",
                "email": "john.doe@example.com",
            },
        )
        patient_id = conn.execute(
            sa.text("SELECT id FROM patients WHERE email = 'john.doe@example.com'")
        ).scalar()

    # --- Ensure a demo appointment exists (tomorrow 10am UTC) ---
    appointment_id = None
    if doctor_id and patient_id:
        appointment_id = conn.execute(
            sa.text(
                """
                SELECT id FROM appointments 
                WHERE patient_id = :pid AND doctor_id = :did
                ORDER BY scheduled_time DESC
                LIMIT 1
                """
            ),
            {"pid": patient_id, "did": doctor_id},
        ).scalar()

        if not appointment_id:
            appt_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
            conn.execute(
                sa.text(
                    """
                    INSERT INTO appointments (patient_id, doctor_id, scheduled_time, notes)
                    VALUES (:pid, :did, :ts, :notes)
                    """
                ),
                {
                    "pid": patient_id,
                    "did": doctor_id,
                    "ts": appt_time,
                    "notes": "Initial consultation (seeded).",
                },
            )
            appointment_id = conn.execute(
                sa.text(
                    """
                    SELECT id FROM appointments
                    WHERE patient_id = :pid AND doctor_id = :did
                    ORDER BY id DESC LIMIT 1
                    """
                ),
                {"pid": patient_id, "did": doctor_id},
            ).scalar()

    # --- Seed a doctor note if possible ---
    if doctor_id and patient_id:
        # Only insert if not already present
        existing_note_id = conn.execute(
            sa.text(
                """
                SELECT id FROM doctor_notes
                WHERE doctor_id = :did AND patient_id = :pid AND content LIKE :content
                LIMIT 1
                """
            ),
            {
                "did": doctor_id,
                "pid": patient_id,
                "content": "%(SEED)% General check-up planned%",
            },
        ).scalar()

        if not existing_note_id:
            conn.execute(
                sa.text(
                    """
                    INSERT INTO doctor_notes (doctor_id, patient_id, appointment_id, content, created_at)
                    VALUES (:did, :pid, :aid, :content, NOW())
                    """
                ),
                {
                    "did": doctor_id,
                    "pid": patient_id,
                    "aid": appointment_id,
                    "content": "(SEED) General check-up planned. Vitals to be reviewed; labs pending.",
                },
            )

    # --- Seed a nurse profile for nurse_anna ---
    if nurse_id:
        existing_profile_id = conn.execute(
            sa.text(
                "SELECT id FROM nurse_profiles WHERE nurse_id = :nid LIMIT 1"
            ),
            {"nid": nurse_id},
        ).scalar()
        if not existing_profile_id:
            conn.execute(
                sa.text(
                    """
                    INSERT INTO nurse_profiles (nurse_id, bio, notes, created_at)
                    VALUES (:nid, :bio, :notes, NOW())
                    """
                ),
                {
                    "nid": nurse_id,
                    "bio": "Experienced RN specializing in patient triage and follow-up.",
                    "notes": "(SEED) Onboards new patients and manages pre-visit questionnaires.",
                },
            )


def downgrade():
    conn = op.get_bind()

    # Remove seeded doctor note(s)
    conn.execute(
        sa.text(
            "DELETE FROM doctor_notes WHERE content LIKE :content"
        ),
        {"content": "%(SEED)% General check-up planned%"},
    )

    # Remove seeded nurse profile
    # (only the one we created; keep any manually created profiles)
    nurse_user_id = conn.execute(
        sa.text("SELECT id FROM users WHERE username = 'nurse_anna'")
    ).scalar()
    if nurse_user_id:
        nurse_id = conn.execute(
            sa.text("SELECT id FROM nurses WHERE user_id = :uid"),
            {"uid": nurse_user_id},
        ).scalar()
        if nurse_id:
            conn.execute(
                sa.text("DELETE FROM nurse_profiles WHERE nurse_id = :nid"),
                {"nid": nurse_id},
            )

    # Optional: remove the demo appointment/patient we created (only if we created them)
    # Safer to leave them, but if you want to clean: uncomment below.
    # conn.execute(sa.text("DELETE FROM appointments WHERE notes = 'Initial consultation (seeded).'"))
    # conn.execute(sa.text("DELETE FROM patients WHERE email = 'john.doe@example.com'"))
