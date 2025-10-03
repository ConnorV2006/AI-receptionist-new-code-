"""Seed demo patients, appointments, and doctor notes

Revision ID: 0012_seed_demo_data
Revises: 0011_add_doctor_time_composite
Create Date: 2025-10-03

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# Revision identifiers, used by Alembic.
revision = "0012_seed_demo_data"
down_revision = "0011_add_doctor_time_composite"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Insert demo patients
    conn.execute(
        sa.text(
            """
            INSERT INTO patients (first_name, last_name, email, phone, date_of_birth)
            VALUES
                ('Alice', 'Smith', 'alice.smith@example.com', '+15550000001', '1990-01-01'),
                ('Bob', 'Johnson', 'bob.johnson@example.com', '+15550000002', '1985-05-12'),
                ('Charlie', 'Brown', 'charlie.brown@example.com', '+15550000003', '1978-09-23')
            ON CONFLICT DO NOTHING;
            """
        )
    )

    # Insert demo appointments for doctor_id=1
    conn.execute(
        sa.text(
            """
            INSERT INTO appointments (patient_id, doctor_id, scheduled_time, status, reason)
            SELECT p.id, 1, NOW() + (i * interval '1 day'), 'scheduled', 'Routine check-up'
            FROM patients p, generate_series(1, 3) g(i)
            ON CONFLICT DO NOTHING;
            """
        )
    )

    # Insert demo doctor notes linked to doctor_id=1
    conn.execute(
        sa.text(
            """
            INSERT INTO doctor_notes (doctor_id, patient_id, note, created_at)
            SELECT 1, p.id, 'Initial consultation notes for ' || p.first_name, NOW()
            FROM patients p
            ON CONFLICT DO NOTHING;
            """
        )
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM doctor_notes WHERE doctor_id = 1;"))
    conn.execute(sa.text("DELETE FROM appointments WHERE doctor_id = 1;"))
    conn.execute(
        sa.text(
            "DELETE FROM patients WHERE email IN ('alice.smith@example.com', 'bob.johnson@example.com', 'charlie.brown@example.com');"
        )
    )
