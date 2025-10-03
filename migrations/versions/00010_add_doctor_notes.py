"""Add doctor_notes table"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0010_add_doctor_notes"
down_revision = "0009_seed_audit_logs"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "doctor_note",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patient.id"), nullable=False),
        sa.Column("appointment_id", sa.Integer, sa.ForeignKey("appointment.id")),
        sa.Column("note", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("doctor_note")
