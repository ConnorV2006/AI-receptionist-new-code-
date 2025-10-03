"""Initial full schema + indexes + rich demo seed (past, present, future, Twilio logs)

Revision ID: 0001_initial_full
Revises:
Create Date: 2025-10-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, DateTime, Text, func


# Revision identifiers
revision = "0001_initial_full"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ----------------------------
    # Tables
    # ----------------------------
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(120), unique=True),
        sa.Column("password_hash", sa.String(128), nullable=False),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id")),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False, index=True),
        sa.Column("email", sa.String(120), unique=True, index=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("dob", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("scheduled_time", sa.DateTime, nullable=False),
        sa.Column("notes", sa.Text),
        sa.Column("status", sa.String(20), server_default="scheduled"),
    )

    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(255)),
        sa.Column("timestamp", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "nurse_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nurse_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("department", sa.String(100)),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    # ----------------------------
    # Indexes
    # ----------------------------
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_created_at", "users", ["created_at"])
    op.create_index("ix_appointments_doctor_time", "appointments", ["doctor_id", "scheduled_time"])
    op.create_index("ix_doctor_notes_doctor_id", "doctor_notes", ["doctor_id"])
    op.create_index("ix_doctor_notes_patient_id", "doctor_notes", ["patient_id"])
    op.create_index("ix_doctor_notes_created_at", "doctor_notes", ["created_at"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("ix_nurse_profiles_nurse_id", "nurse_profiles", ["nurse_id"])

    # ----------------------------
    # Seed Data
    # ----------------------------
    roles = table("roles", column("id", Integer), column("name", String))
    users = table("users",
        column("id", Integer),
        column("username", String),
        column("email", String),
        column("password_hash", String),
        column("role_id", Integer),
    )
    patients = table("patients",
        column("id", Integer),
        column("first_name", String),
        column("last_name", String),
        column("email", String),
        column("phone", String),
    )
    appointments = table("appointments",
        column("id", Integer),
        column("patient_id", Integer),
        column("doctor_id", Integer),
        column("scheduled_time", DateTime),
        column("notes", Text),
        column("status", String),
    )
    doctor_notes = table("doctor_notes",
        column("id", Integer),
        column("doctor_id", Integer),
        column("patient_id", Integer),
        column("content", Text),
    )
    audit_logs = table("audit_logs",
        column("id", Integer),
        column("user_id", Integer),
        column("action", String),
    )
    nurse_profiles = table("nurse_profiles",
        column("id", Integer),
        column("nurse_id", Integer),
        column("department", String),
    )

    # Roles
    op.bulk_insert(roles, [
        {"id": 1, "name": "Admin"},
        {"id": 2, "name": "Doctor"},
        {"id": 3, "name": "Nurse"},
        {"id": 4, "name": "Receptionist"},
    ])

    # Users
    op.bulk_insert(users, [
        {"id": 1, "username": "admin", "email": "admin@example.com", "password_hash": "hash", "role_id": 1},
        {"id": 2, "username": "drsmith", "email": "drsmith@example.com", "password_hash": "hash", "role_id": 2},
        {"id": 3, "username": "nursejane", "email": "nursejane@example.com", "password_hash": "hash", "role_id": 3},
        {"id": 4, "username": "reception", "email": "reception@example.com", "password_hash": "hash", "role_id": 4},
    ])

    # Patients
    op.bulk_insert(patients, [
        {"id": 1, "first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "555-1234"},
        {"id": 2, "first_name": "Jane", "last_name": "Smith", "email": "jane@example.com", "phone": "555-5678"},
        {"id": 3, "first_name": "Carlos", "last_name": "Martinez", "email": "carlos@example.com", "phone": "555-2468"},
    ])

    # Appointments
    op.bulk_insert(appointments, [
        {"id": 1, "patient_id": 1, "doctor_id": 2, "scheduled_time": func.now() - sa.text("interval '7 days'"), "notes": "Follow-up after surgery", "status": "completed"},
        {"id": 2, "patient_id": 2, "doctor_id": 2, "scheduled_time": func.now() - sa.text("interval '2 days'"), "notes": "Flu symptoms check", "status": "completed"},
        {"id": 3, "patient_id": 1, "doctor_id": 2, "scheduled_time": func.now(), "notes": "Annual check-up", "status": "scheduled"},
        {"id": 4, "patient_id": 2, "doctor_id": 2, "scheduled_time": func.now(), "notes": "Follow-up visit", "status": "scheduled"},
        {"id": 5, "patient_id": 3, "doctor_id": 2, "scheduled_time": func.now(), "notes": "New patient intake", "status": "scheduled"},
        {"id": 6, "patient_id": 1, "doctor_id": 2, "scheduled_time": func.now() + sa.text("interval '1 day'"), "notes": "Lab results discussion", "status": "scheduled"},
        {"id": 7, "patient_id": 2, "doctor_id": 2, "scheduled_time": func.now() + sa.text("interval '7 days'"), "notes": "1 week follow-up", "status": "scheduled"},
    ])

    # Doctor notes
    op.bulk_insert(doctor_notes, [
        {"id": 1, "doctor_id": 2, "patient_id": 1, "content": "Post-surgery recovery progressing well."},
        {"id": 2, "doctor_id": 2, "patient_id": 2, "content": "Patient had flu, advised rest and hydration."},
        {"id": 3, "doctor_id": 2, "patient_id": 3, "content": "Initial consultation completed, labs pending."},
    ])

    # Audit logs (with Twilio samples: SMS, Calls, Fax)
    op.bulk_insert(audit_logs, [
        {"id": 1, "user_id": 1, "action": "System initialized with base schema"},
        # Past
        {"id": 2, "user_id": 2, "action": "Completed appointment for John Doe (7 days ago)"},
        {"id": 3, "user_id": 2, "action": "Completed appointment for Jane Smith (2 days ago)"},
        {"id": 4, "user_id": 4, "action": "SMS sent via Twilio: 'Your appointment has been completed.' (2 days ago)"},
        {"id": 5, "user_id": 4, "action": "Inbound patient call missed (John Doe, 6 days ago)"},
        {"id": 6, "user_id": 1, "action": "Faxed lab results to Carlos Martinez (5 days ago)"},
        # Today
        {"id": 7, "user_id": 4, "action": "Checked in John Doe for annual check-up (today)"},
        {"id": 8, "user_id": 3, "action": "Nurse Jane updated vitals for Carlos Martinez (today)"},
        {"id": 9, "user_id": 4, "action": "SMS reminder sent via Twilio: 'Your appointment is today at 3 PM.'"},
        {"id": 10, "user_id": 2, "action": "Inbound call transferred to Dr. Smith via Twilio Voice (Jane Smith)"},
        {"id": 11, "user_id": 4, "action": "Fax confirmation received for lab order (today)"},
        # Future
        {"id": 12, "user_id": 2, "action": "Scheduled follow-up for Jane Smith (in 7 days)"},
        {"id": 13, "user_id": 2, "action": "Scheduled lab results discussion for John Doe (tomorrow)"},
        {"id": 14, "user_id": 4, "action": "Automated SMS scheduled: 'Reminder: Appointment tomorrow at 10 AM.'"},
        {"id": 15, "user_id": 4, "action": "Automated call scheduled to Jane Smith for appointment confirmation (in 3 days)"},
        {"id": 16, "user_id": 1, "action": "Fax queued for insurance paperwork submission (in 2 days)"},
    ])

    # Nurse & Receptionist profiles
    op.bulk_insert(nurse_profiles, [
        {"id": 1, "nurse_id": 3, "department": "General Medicine"},
        {"id": 2, "nurse_id": 4, "department": "Front Desk / Reception"},
    ])


def downgrade():
    op.drop_table("nurse_profiles")
    op.drop_table("audit_logs")
    op.drop_table("doctor_notes")
    op.drop_table("appointments")
    op.drop_table("patients")
    op.drop_table("users")
    op.drop_table("roles")
