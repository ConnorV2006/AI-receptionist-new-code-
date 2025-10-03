"""Add doctor notes and doctor_id to appointments

Revision ID: 0007_add_doctor_notes
Revises: 0006_roles
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "0007_add_doctor_notes"
down_revision = "0006_roles"
branch_labels = None
depends_on = None


def upgrade():
    # Add doctor_id column to appointments
    op.add_column("appointment", sa.Column("doctor_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_appointment_doctor", "appointment", "user", ["doctor_id"], ["id"])

    # Create notes table
    op.create_table(
        "note",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient.id")),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table("note")
    op.drop_constraint("fk_appointment_doctor", "appointment", type_="foreignkey")
    op.drop_column("appointment", "doctor_id")
