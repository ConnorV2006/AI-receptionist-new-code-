"""Seed demo data for roles, users, patients, appointments, notes, nurse/receptionist profiles, and Twilio logs

Revision ID: 0002_seed_demo_data
Revises: 0001_initial_full
Create Date: 2025-10-04
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# Revision identifiers
revision = "0002_seed_demo_data"
down_revision = "0001_initial_full"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # ----------------------
    # Roles
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO roles (id, name) VALUES
        (1, 'Admin'),
        (2, 'Doctor'),
        (3, 'Nurse'),
        (4, 'Receptionist')
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Users
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO users (id, username, email, password_hash, role_id, created_at) VALUES
        (1, 'admin', 'admin@example.com', 'hashed_pw', 1, NOW()),
        (2, 'drsmith', 'drsmith@example.com', 'hashed_pw', 2, NOW()),
        (3, 'nursejane', 'nursejane@example.com', 'hashed_pw', 3, NOW()),
        (4, 'receptionbob', 'receptionbob@example.com', 'hashed_pw', 4, NOW())
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Patients
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO patients (id, first_name, last_name, email, phone, date_of_birth) VALUES
        (1, 'John', 'Doe', 'johndoe@example.com', '+1555000111', '1990-01-01'),
        (2, 'Jane', 'Smith', 'janesmith@example.com', '+1555000222', '1985-05-20'),
        (3, 'Michael', 'Johnson', 'michaelj@example.com', '+1555000333', '1978-10-10')
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Appointments
    # ----------------------
    now = datetime.utcnow()
    today_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    today_2pm = now.replace(hour=14, minute=0, second=0, microsecond=0)
    tomorrow_10am = today_9am + timedelta(days=1, hours=1)

    conn.execute(sa.text("""
        INSERT INTO appointments (id, patient_id, doctor_id, scheduled_time, reason) VALUES
        (1, 1, 2, :t1, 'General checkup'),
        (2, 2, 2, :t2, 'Follow-up consultation'),
        (3, 3, 2, :t3, 'Blood test and review')
        ON CONFLICT (id) DO NOTHING;
    """), {"t1": today_9am, "t2": today_2pm, "t3": tomorrow_10am})

    # ----------------------
    # Doctor Notes
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO doctor_notes (id, patient_id, doctor_id, note, created_at) VALUES
        (1, 1, 2, 'Patient reports mild headaches. Recommended hydration and rest.', NOW() - INTERVAL '2 days'),
        (2, 2, 2, 'Follow-up shows improved condition.', NOW() - INTERVAL '1 day'),
        (3, 3, 2, 'Pending lab results. Will review tomorrow.', NOW())
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Nurse Profiles
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO nurse_profiles (id, user_id, nurse_id) VALUES
        (1, 3, 'NURSE001')
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Receptionist Profiles
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO receptionist_profiles (id, user_id, receptionist_id) VALUES
        (1, 4, 'RECEP001')
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Audit Logs
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO audit_logs (id, user_id, action, timestamp) VALUES
        (1, 1, 'Created initial demo data', NOW()),
        (2, 2, 'Doctor reviewed patient note', NOW() - INTERVAL '1 hour'),
        (3, 4, 'Receptionist scheduled appointment', NOW() - INTERVAL '30 minutes')
        ON CONFLICT (id) DO NOTHING;
    """))

    # ----------------------
    # Twilio Logs (SMS, Calls, Fax)
    # ----------------------
    conn.execute(sa.text("""
        INSERT INTO twilio_logs (id, type, direction, from_number, to_number, content, status, timestamp) VALUES
        (1, 'sms', 'inbound', '+15557654321', '+1555000111', 'Hello, I need to confirm my appointment.', 'received', NOW() - INTERVAL '2 days'),
        (2, 'sms', 'outbound', '+1555000222', '+15557654321', 'Your appointment is confirmed for tomorrow at 10 AM.', 'sent', NOW() - INTERVAL '1 day'),
        (3, 'call', 'inbound', '+15557650000', '+1555000111', 'Incoming call from patient about test results.', 'completed', NOW() - INTERVAL '3 hours'),
        (4, 'call', 'outbound', '+1555000111', '+15557650000', 'Follow-up call regarding lab results.', 'completed', NOW() - INTERVAL '1 hour'),
        (5, 'fax', 'inbound', '+15559998888', '+1555000222', 'Lab results fax received.', 'completed', NOW() - INTERVAL '5 hours'),
        (6, 'fax', 'outbound', '+1555000222', '+15559998888', 'Fax sent with prescription update.', 'completed', NOW() + INTERVAL '1 day')
        ON CONFLICT (id) DO NOTHING;
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM twilio_logs WHERE id <= 6;"))
    conn.execute(sa.text("DELETE FROM audit_logs WHERE id <= 3;"))
    conn.execute(sa.text("DELETE FROM receptionist_profiles WHERE id = 1;"))
    conn.execute(sa.text("DELETE FROM nurse_profiles WHERE id = 1;"))
    conn.execute(sa.text("DELETE FROM doctor_notes WHERE id <= 3;"))
    conn.execute(sa.text("DELETE FROM appointments WHERE id <= 3;"))
    conn.execute(sa.text("DELETE FROM patients WHERE id <= 3;"))
    conn.execute(sa.text("DELETE FROM users WHERE id <= 4;"))
    conn.execute(sa.text("DELETE FROM roles WHERE id <= 4;"))
