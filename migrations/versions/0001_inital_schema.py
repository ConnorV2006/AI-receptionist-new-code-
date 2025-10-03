"""Initial schema"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(120), unique=True, nullable=False),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="receptionist"),
    )

    op.create_table(
        "patient",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(120)),
        sa.Column("phone", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "appointment",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patient.id"), nullable=False),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user", sa.String(120)),
        sa.Column("action", sa.String(255)),
        sa.Column("details", sa.Text),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("audit_log")
    op.drop_table("appointment")
    op.drop_table("patient")
    op.drop_table("user")
