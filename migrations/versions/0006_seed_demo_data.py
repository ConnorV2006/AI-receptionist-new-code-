"""Seed demo clinic, patients, appointments, notes, calls, and messages"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
import datetime

# Revision identifiers, used by Alembic
revision = '0006_seed_demo_data'
down_revision = '0005_seed_doctor'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()

    # --- Insert a sample clinic ---
    conn.execute(sa.text("""
        INSERT INTO clinic (slug, twilio_number, twilio_sid, twilio_token)
        VALUES ('demo-clinic', '+15555550100', 'demoSID123', 'demoTOKEN456')
    """))

    # --- Insert sample patients ---
    conn.execute(sa.text("""
        INSERT INTO patient (name, phone, email, clinic_id)
        VALUES 
          ('Alice Johnson', '+15555550101', 'alice@example.com', 1),
          ('Bob Smith', '+15555550102', 'bob@example.com', 1),
          ('Carol Davis', '+15555550103', 'carol@example.com', 1)
    """))

    # --- Insert sample appointments ---
    now = datetime.datetime.utcnow()
    conn.execute(sa.text("""
        INSERT INTO appointment (patient_id, doctor_id, clinic_id, time, reason)
        VALUES 
          (1, 1, 1, :appt1, 'Routine Checkup'),
          (2, 1, 1, :appt2, 'Follow-up Consultation'),
          (3, 1, 1, :appt3, 'Lab Results Review')
    """), {
        "appt1": now + datetime.timedelta(days=1),
        "appt2": now + datetime.timedelta(days=2),
        "appt3": now + datetime.timedelta(days=3),
    })

    # --- Insert doctor notes ---
    conn.execute(sa.text("""
        INSERT INTO doctors_note (appointment_id, doctor_id, note)
        VALUES 
          (1, 1, 'Patient healthy, return in 6 months'),
          (2, 1, 'Prescribed medication adjustment'),
          (3, 1, 'Discussed lab results, all within normal range')
    """))

    # --- Insert messages ---
    conn.execute(sa.text("""
        INSERT INTO message (patient_id, clinic_id, content, direction)
        VALUES 
          (1, 1, 'Hi, I want to confirm my appointment tomorrow.', 'inbound'),
          (1, 1, 'Your appointment is confirmed. See you tomorrow!', 'outbound'),
          (2, 1, 'Can I reschedule?', 'inbound')
    """))

    # --- Insert phone calls ---
    conn.execute(sa.text("""
        INSERT INTO call (patient_id, clinic_id, status, duration)
        VALUES
          (1, 1, 'completed', 180),
          (2, 1, 'missed', 0),
          (3, 1, 'completed', 240)
    """))

def downgrade():
    conn = op.get_bind()

    # Delete inserted sample data
    conn.execute(sa.text("DELETE FROM call"))
    conn.execute(sa.text("DELETE FROM message"))
    conn.execute(sa.text("DELETE FROM doctors_note"))
    conn.execute(sa.text("DELETE FROM appointment"))
    conn.execute(sa.text("DELETE FROM patient"))
    conn.execute(sa.text("DELETE FROM clinic WHERE slug = 'demo-clinic'"))
