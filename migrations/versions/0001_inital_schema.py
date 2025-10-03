"""Initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(64), nullable=False, unique=True)
    )

    op.create_table("user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("clinic",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("patient",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("dob", sa.Date()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("appointment",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient.id")),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("scheduled_for", sa.DateTime(), nullable=False),
        sa.Column("reason", sa.String(255)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("note",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient.id")),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("call_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
        sa.Column("from_number", sa.String(20)),
        sa.Column("to_number", sa.String(20)),
        sa.Column("status", sa.String(20)),
        sa.Column("duration", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("message_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")),
        sa.Column("from_number", sa.String(20)),
        sa.Column("to_number", sa.String(20)),
        sa.Column("body", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table("audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table("audit_log")
    op.drop_table("message_log")
    op.drop_table("call_log")
    op.drop_table("note")
    op.drop_table("appointment")
    op.drop_table("patient")
    op.drop_table("clinic")
    op.drop_table("user")
    op.drop_table("role")
