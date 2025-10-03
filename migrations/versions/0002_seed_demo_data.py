"""Seed demo patients, appointments, notes, nurse/receptionist profiles, and Twilio logs

Revision ID: 0002_seed_demo_data
Revises: 0001_initial_full
Create Date: 2025-10-03
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = "0002_seed_demo_data"
down_revision = "0001_initial_full"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # --- Patients ---
    conn.execute(
        sa.text(
            """
            INSERT INTO patients (first_name, last_name, email, phone, date_of_birth)
            VALUES
                ('Alice', 'Johnson', 'alice@example.com', '5551112222', '1990-05-14'),
                ('Bob', 'Smith', 'bob@example.com', '5553334444', '1985-08-23'),
                ('Charlie', 'Brown', 'charlie@example.com', '5556667777', '1978-11-30')
            """
        )
    )

    # --- Appointments (past, today, future) ---
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)

    conn.execute(
        sa.text(
            """
            INSERT INTO appointments (patient_id, doctor_id, scheduled_time, reason)
            VALUES
                (1, 42, :yesterday, 'Follow-up visit'),
                (2, 42, :now, 'General consultation'),
                (3, 42, :tomorrow, 'Routine check-up')
            """
        ),
        {"yesterday": yesterday, "now": now, "tomorrow": tomorrow},
    )

    # --- Doctor Notes ---
    conn.execute(
        sa.text(
            """
            INSERT INTO doctor_notes (patient_id, doctor_id, note, created_at)
            VALUES
                (1, 42, 'Patient recovering well, no complications.', :yesterday),
                (2, 42, 'Discussed lifestyle changes, scheduled blood test.', :now),
                (3, 42, 'Initial consultation for new patient.', :tomorrow)
            """
        ),
        {"yesterday": yesterday, "now": now, "tomorrow": tomorrow},
    )

    # --- Nurse Profiles ---
    conn.execute(
        sa.text(
            """
            INSERT INTO nurse_profiles (user_id, nurse_id)
            VALUES
                (1, 'NURSE-001'),
                (2, 'NURSE-002')
            """
        )
    )

    # --- Receptionist Profiles ---
    conn.execute(
        sa.text(
            """
            INSERT INTO receptionist_profiles (user_id, receptionist_id)
            VALUES
                (3, 'RECEP-001')
            """
        )
    )

    # --- Twilio Logs (SMS, Call, Fax – past, now, future) ---
    conn.execute(
        sa.text(
            """
            INSERT INTO twilio_logs (type, direction, from_number, to_number, content, status, timestamp)
            VALUES
                -- Past SMS
                ('sms', 'inbound', '+15551112222', '+15553334444', 'Hello, I need to reschedule.', 'delivered', :yesterday),
                -- Present SMS
                ('sms', 'outbound', '+15553334444', '+15551112222', 'Confirmed your appointment today at 2PM.', 'sent', :now),
                -- Future SMS
                ('sms', 'outbound', '+15553334444', '+15556667777', 'Reminder: Appointment tomorrow.', 'queued', :tomorrow),

                -- Past Call
                ('call', 'inbound', '+15558889999', '+15553334444', 'Patient called with chest pain concerns.', 'completed', :yesterday),
                -- Present Call
                ('call', 'outbound', '+15553334444', '+15559990000', 'Doctor called patient for consultation.', 'in-progress', :now),
                -- Future Call
                ('call', 'outbound', '+15553334444', '+15551110000', 'Scheduled check-in call.', 'queued', :tomorrow),

                -- Past Fax
                ('fax', 'inbound', '+15557778888', '+15553334444', 'Lab results faxed.', 'completed', :yesterday),
                -- Present Fax
                ('fax', 'outbound', '+15553334444', '+15556667777', 'Sending referral letter.', 'sending', :now),
                -- Future Fax
                ('fax', 'outbound', '+15553334444', '+15554443333', 'Planned fax of prescription.', 'queued', :tomorrow)
            """
        ),
        {"yesterday": yesterday, "now": now, "tomorrow": tomorrow},
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM twilio_logs"))
    conn.execute(sa.text("DELETE FROM receptionist_profiles"))
    conn.execute(sa.text("DELETE FROM nurse_profiles"))
    conn.execute(sa.text("DELETE FROM doctor_notes"))
    conn.execute(sa.text("DELETE FROM appointments"))
    conn.execute(sa.text("DELETE FROM patients"))
