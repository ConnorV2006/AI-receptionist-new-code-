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
    connection = op.get_bind()

    # Insert demo patients
    patients = [
        {"id": 1, "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"},
        {"id": 2, "first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"},
    ]
    op.bulk_insert(
        sa.table(
            "patients",
            sa.column("id", sa.Integer),
            sa.column("first_name", sa.String),
            sa.column("last_name", sa.String),
            sa.column("email", sa.String),
        ),
        patients,
    )

    # Insert demo appointments (doctor_id 1 assumed)
    now = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)
    appointments = [
        {"id": 1, "patient_id": 1, "doctor_id": 1, "scheduled_time": now},
        {"id": 2, "patient_id": 2, "doctor_id": 1, "scheduled_time": now + timedelta(hours=1)},
    ]
    op.bulk_insert(
        sa.table(
            "appointments",
            sa.column("id", sa.Integer),
            sa.column("patient_id", sa.Integer),
            sa.column("doctor_id", sa.Integer),
            sa.column("scheduled_time", sa.DateTime),
        ),
        appointments,
    )

    # Insert demo doctor notes
    notes = [
        {
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_id": 1,
            "note": "Routine checkup. Patient doing well.",
            "created_at": now,
        },
        {
            "id": 2,
            "patient_id": 2,
            "doctor_id": 1,
            "appointment_id": 2,
            "note": "Follow-up visit scheduled.",
            "created_at": now + timedelta(hours=1),
        },
    ]
    op.bulk_insert(
        sa.table(
            "doctor_notes",
            sa.column("id", sa.Integer),
            sa.column("patient_id", sa.Integer),
            sa.column("doctor_id", sa.Integer),
            sa.column("appointment_id", sa.Integer),
            sa.column("note", sa.Text),
            sa.column("created_at", sa.DateTime),
        ),
        notes,
    )


def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM doctor_notes WHERE id IN (1,2)"))
    connection.execute(sa.text("DELETE FROM appointments WHERE id IN (1,2)"))
    connection.execute(sa.text("DELETE FROM patients WHERE id IN (1,2)"))
