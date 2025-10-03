"""Initial full schema with demo data for AI Receptionist

Revision ID: 0001_initial_full
Revises: 
Create Date: 2025-10-03
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers, used by Alembic
revision = "0001_initial_full"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ----------------------------
    # Roles
    # ----------------------------
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
    )

    # ----------------------------
    # Users
    # ----------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(64), unique=True, nullable=False),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(128)),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id")),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_created_at", "users", ["created_at"])

    # ----------------------------
    # Patients
    # ----------------------------
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(64), nullable=False),
        sa.Column("last_name", sa.String(64), nullable=False),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("phone", sa.String(20)),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_patients_last_name", "patients", ["last_name"])
    op.create_index("ix_patients_email", "patients", ["email"])

    # ----------------------------
    # Appointments
    # ----------------------------
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("scheduled_time", sa.DateTime, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_scheduled_time", "appointments", ["scheduled_time"])
    op.create_index(
        "ix_appointments_doctor_time",
        "appointments",
        ["doctor_id", "scheduled_time"],
    )

    # ----------------------------
    # Doctor Notes
    # ----------------------------
    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_doctor_notes_doctor_id", "doctor_notes", ["doctor_id"])
    op.create_index("ix_doctor_notes_patient_id", "doctor_notes", ["patient_id"])
    op.create_index("ix_doctor_notes_created_at", "doctor_notes", ["created_at"])

    # ----------------------------
    # Nurse Profiles
    # ----------------------------
    op.create_table(
        "nurse_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nurse_id", sa.Integer, sa.ForeignKey("users.id"), unique=True, nullable=False),
        sa.Column("department", sa.String(120)),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_nurse_profiles_nurse_id", "nurse_profiles", ["nurse_id"])

    # ----------------------------
    # Audit Logs
    # ----------------------------
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(256)),
        sa.Column("details", sa.Text),
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])

    # ----------------------------
    # Twilio Logs
    # ----------------------------
    op.create_table(
        "twilio_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),  # sms, call, fax
        sa.Column("from_number", sa.String(20), nullable=False),
        sa.Column("to_number", sa.String(20), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(50)),
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow),
    )
    op.create_index("ix_twilio_logs_type", "twilio_logs", ["type"])
    op.create_index("ix_twilio_logs_timestamp", "twilio_logs", ["timestamp"])

    # ----------------------------
    # DEMO DATA
    # ----------------------------
    conn = op.get_bind()

    # Insert Roles
    roles = ["Admin", "Doctor", "Nurse", "Receptionist", "Patient"]
    for i, r in enumerate(roles, start=1):
        conn.execute(sa.text("INSERT INTO roles (id, name) VALUES (:id, :name)"), {"id": i, "name": r})

    # Insert Users
    conn.execute(sa.text(
        "INSERT INTO users (id, username, email, password_hash, role_id, created_at) VALUES "
        "(1, 'admin', 'admin@example.com', 'hashed_pw', 1, :now),"
        "(2, 'dr_smith', 'drsmith@example.com', 'hashed_pw', 2, :now),"
        "(3, 'nurse_jane', 'nursejane@example.com', 'hashed_pw', 3, :now),"
        "(4, 'reception_bob', 'reception@example.com', 'hashed_pw', 4, :now),"
        "(5, 'patient_mike', 'patient@example.com', 'hashed_pw', 5, :now)"
    ), {"now": datetime.utcnow()})

    # Insert Patient
    conn.execute(sa.text(
        "INSERT INTO patients (id, first_name, last_name, email, phone, created_at) VALUES "
        "(1, 'Mike', 'Johnson', 'patient@example.com', '+155555501', :now)"
    ), {"now": datetime.utcnow()})

    # Insert Appointments (past, present, future)
    now = datetime.utcnow()
    appointments = [
        (1, 1, 2, now - timedelta(days=1)),  # past
        (2, 1, 2, now),                      # present
        (3, 1, 2, now + timedelta(days=1)),  # future
    ]
    for a in appointments:
        conn.execute(sa.text(
            "INSERT INTO appointments (id, patient_id, doctor_id, scheduled_time, created_at) VALUES "
            "(:id, :patient_id, :doctor_id, :scheduled_time, :created_at)"
        ), {"id": a[0], "patient_id": a[1], "doctor_id": a[2], "scheduled_time": a[3], "created_at": now})

    # Insert Doctor Notes
    conn.execute(sa.text(
        "INSERT INTO doctor_notes (id, doctor_id, patient_id, content, created_at) VALUES "
        "(1, 2, 1, 'Patient reported mild headache yesterday.', :now1),"
        "(2, 2, 1, 'Follow-up visit today showed improvement.', :now2),"
        "(3, 2, 1, 'Scheduled future check-up.', :now3)"
    ), {"now1": now - timedelta(days=1), "now2": now, "now3": now + timedelta(days=1)})

    # Insert Nurse Profile
    conn.execute(sa.text(
        "INSERT INTO nurse_profiles (id, nurse_id, department, created_at) VALUES "
        "(1, 3, 'General Care', :now)"
    ), {"now": now})

    # Insert Audit Logs
    conn.execute(sa.text(
        "INSERT INTO audit_logs (id, user_id, action, details, timestamp) VALUES "
        "(1, 4, 'Created appointment', 'Reception booked patient appointment', :now1),"
        "(2, 2, 'Added note', 'Doctor added patient note', :now2),"
        "(3, 3, 'Checked vitals', 'Nurse checked patient vitals', :now3)"
    ), {"now1": now - timedelta(hours=2), "now2": now, "now3": now + timedelta(hours=2)})

    # Insert Twilio Logs (SMS, Call, Fax — past, present, future)
    conn.execute(sa.text(
        "INSERT INTO twilio_logs (id, type, from_number, to_number, content, status, timestamp) VALUES "
        "(1, 'sms', '+1234567890', '+155555501', 'Your appointment was yesterday', 'delivered', :past),"
        "(2, 'call', '+1234567890', '+155555501', 'Reminder: Appointment today', 'completed', :present),"
        "(3, 'fax', '+1234567890', '+155555501', 'Lab results sent for tomorrow visit', 'sent', :future)"
    ), {"past": now - timedelta(days=1), "present": now, "future": now + timedelta(days=1)})


def downgrade():
    op.drop_table("twilio_logs")
    op.drop_table("audit_logs")
    op.drop_table("nurse_profiles")
    op.drop_table("doctor_notes")
    op.drop_table("appointments")
    op.drop_table("patients")
    op.drop_table("users")
    op.drop_table("roles")
