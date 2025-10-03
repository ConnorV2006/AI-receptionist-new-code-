"""Add nurse profile table"""

from alembic import op
import sqlalchemy as sa

revision = "0007_add_nurse_profile"
down_revision = "0006_seed_demo_data"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nurse",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False, unique=True),
        sa.Column("specialty", sa.String(120)),
        sa.Column("shift", sa.String(50)),
        sa.Column("license_number", sa.String(50)),
    )


def downgrade():
    op.drop_table("nurse")
