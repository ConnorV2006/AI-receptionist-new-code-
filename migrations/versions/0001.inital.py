"""Initial database setup

Revision ID: 0001_initial
Revises: 
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Roles
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
    )

    # Users
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=120), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role.id")),
    )

    # Clinics
    op.create_table(
        "clinic",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(100), unique=True, nullable=False),
        sa.Column("twilio_number", sa.String(20)),
        sa.Column("twilio_sid", sa.String(100)),
        sa.Column("twilio_token", sa.String(100)),
    )

    # Patients
    op.create_table(
        "patient",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("dob", sa.Date),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
    )

    # Visits
    op.create_table(
        "visit",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient.id")),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Paystubs
    op.create_table(
        "paystub",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("uploaded_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("file_path", sa.String(200)),
    )

    # Appointments
    op.create_table(
        "appointment",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient.id")),
        sa.Column("scheduled_for", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Reminders
    op.create_table(
        "reminder",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("appointment_id", sa.Integer(), sa.ForeignKey("appointment.id")),
        sa.Column("message", sa.String(255)),
        sa.Column("sent_at", sa.DateTime()),
    )

    # File uploads
    op.create_table(
        "file_upload",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("filename", sa.String(200)),
        sa.Column("uploaded_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Call logs
    op.create_table(
        "call_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
        sa.Column("from_number", sa.String(20)),
        sa.Column("to_number", sa.String(20)),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("status", sa.String(50)),
    )

    # Message logs
    op.create_table(
        "message_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
        sa.Column("from_number", sa.String(20)),
        sa.Column("to_number", sa.String(20)),
        sa.Column("body", sa.Text),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now()),
    )

    # Audit logs
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("action", sa.String(200), nullable=False),
        sa.Column("details", sa.Text),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("audit_log")
    op.drop_table("message_log")
    op.drop_table("call_log")
    op.drop_table("file_upload")
    op.drop_table("reminder")
    op.drop_table("appointment")
    op.drop_table("paystub")
    op.drop_table("visit")
    op.drop_table("patient")
    op.drop_table("clinic")
    op.drop_table("user")
    op.drop_table("role")
