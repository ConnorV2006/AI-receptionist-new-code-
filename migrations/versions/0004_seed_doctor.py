"""Seed doctor"""

from alembic import op
import sqlalchemy as sa

revision = "0004_seed_doctor"
down_revision = "0003_seed_receptionist"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO "user" (username, email, password, role)
        VALUES ('doctor1', 'doctor1@example.com',
        'scrypt:32768:8:1$dU8TxvH9BxtdJB2f$3e364efc28cd0961fdf2277bee34a0677aeffbdd034b59d5cd173cff3e8b13b1e981a5b5eaef51925fc9026c732c2a39e276511a0b003b7d36b6959496ef7c91',
        'doctor')
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='doctor'"))
