"""Seed demo data for roles, users, patients, appointments, notes, and Twilio logs

Revision ID: 0002_seed_demo_data
Revises: 0001_initial_full
Create Date: 2025-10-03
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

    # Insert Roles
    conn.execute(sa.text("""
        INSERT INTO roles (name) VALUES
        ('Admin'),
        ('Doctor'),
        ('Nurse'),
        ('Receptionist')
        ON CONFLICT (name) DO NOTHING;
    """))

    # Insert Users
    conn.execute(sa.text("""
        INSERT INTO users (username, email, password, role_id, created_at)
        VALUES
        ('admin', 'admin@example.com', 'hashed_pw', 
            (SELECT id FROM roles WHERE name='Admin'), NOW()),
        ('dr_smith', 'drsmith@example.com', 'hashed_pw', 
            (SELECT id FROM roles WHERE name='Doctor'), NOW()),
        ('nurse_jane', 'nursejane@example.com', 'hashed_pw',
            (SELECT id FROM roles WHERE name='Nurse'), NOW()),
        ('reception_bob', 'bob@example.com', 'hashed_pw',
            (SELECT id FROM roles WHERE name='Receptionist'), NOW())
        ON CONFLICT (email) DO NOTHING;
    """))

    # Insert Nurse Profile
    conn.execute(sa.text("""
        INSERT INTO nurse_profiles (user_id, nurse_id)
        VALUES ((SELECT id FROM users WHERE username='nurse_jane'), 'NURSE001')
        ON CONFLICT DO NOTHING;
    """))

    # Insert Receptionist Profile
    conn.execute(sa.text("""
        INSERT INTO receptionist_profiles (user_id, receptionist_id)
        VALUES ((SELECT id FROM users WHERE username='reception_bob'), 'RECEP001')
        ON CONFLICT DO NOTHING;
    """))

    # Insert Patients
    conn.execute(sa.text("""
        INSERT INTO patients (first_name, last_name, email, phone, created_at)
        VALUES
        ('Alice', 'Johnson', 'alice@example.com', '555-1111', NOW()),
        ('Bob', 'Williams', 'bobw@example.com', '555-2222', NOW()),
        ('Carol', 'Davis', 'carol@example.com', '555-3333', NOW())
        ON CONFLICT (email) DO NOTHING;
    """))

    # Insert Appointments (Past, Present, Future)
    now = datetime.utcnow()
    conn.execute(sa.text("""
        INSERT INTO appointments (patient_id, doctor_id, scheduled_time)
        VALUES
        ((SELECT id FROM patients WHERE email='alice@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         :past),
        ((SELECT id FROM patients WHERE email='bobw@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         :today),
        ((SELECT id FROM patients WHERE email='carol@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         :future)
    """), {
        "past": now - timedelta(days=1),
        "today": now,
        "future": now + timedelta(days=1),
    })

    # Insert Doctor Notes
    conn.execute(sa.text("""
        INSERT INTO doctor_notes (patient_id, doctor_id, content, created_at)
        VALUES
        ((SELECT id FROM patients WHERE email='alice@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         'Follow-up visit went well. Patient recovering.', NOW() - interval '1 day'),
        ((SELECT id FROM patients WHERE email='bobw@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         'Initial consultation completed.', NOW()),
        ((SELECT id FROM patients WHERE email='carol@example.com'),
         (SELECT id FROM users WHERE username='dr_smith'),
         'Scheduled for future surgery prep.', NOW() + interval '1 day')
    """))

    # Insert Twilio Logs (SMS, Call, Fax – Past, Present, Future)
    conn.execute(sa.text("""
        INSERT INTO twilio_logs (type, direction, from_number, to_number, content, status, timestamp)
        VALUES
        ('sms', 'inbound', '+15550001', '+15551111', 'Patient Alice confirming appointment.', 'delivered', NOW() - interval '1 day'),
        ('sms', 'outbound', '+15550002', '+15552222', 'Reminder: Appointment today for Bob.', 'sent', NOW()),
        ('sms', 'outbound', '+15550003', '+15553333', 'Reminder: Appointment tomorrow for Carol.', 'queued', NOW() + interval '1 day'),

        ('call', 'inbound', '+15554444', '+15551111', 'Patient Alice called regarding results.', 'completed', NOW() - interval '1 day'),
        ('call', 'outbound', '+15555555', '+15552222', 'Doctor follow-up with Bob.', 'completed', NOW()),
        ('call', 'outbound', '+15556666', '+15553333', 'Pre-surgery call for Carol.', 'scheduled', NOW() + interval '1 day'),

        ('fax', 'inbound', '+15557777', '+15551111', 'Lab results for Alice.', 'received', NOW() - interval '1 day'),
        ('fax', 'outbound', '+15558888', '+15552222', 'Medical records sent for Bob.', 'sent', NOW()),
        ('fax', 'outbound', '+15559999', '+15553333', 'Pre-surgery clearance fax for Carol.', 'pending', NOW() + interval '1 day')
    """))


def downgrade():
    conn = op.get_bind()

    conn.execute(sa.text("DELETE FROM twilio_logs"))
    conn.execute(sa.text("DELETE FROM doctor_notes"))
    conn.execute(sa.text("DELETE FROM appointments"))
    conn.execute(sa.text("DELETE FROM patients"))
    conn.execute(sa.text("DELETE FROM receptionist_profiles"))
    conn.execute(sa.text("DELETE FROM nurse_profiles"))
    conn.execute(sa.text("DELETE FROM users"))
    conn.execute(sa.text("DELETE FROM roles"))
