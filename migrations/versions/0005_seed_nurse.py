"""Seed nurse"""

from alembic import op
import sqlalchemy as sa

revision = "0005_seed_nurse"
down_revision = "0004_seed_doctor"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO "user" (username, email, password, role)
        VALUES ('nurse1', 'nurse1@example.com',
        'scrypt:32768:8:1$vXDD515se4ZoTdZa$6364b2f15825db541b2f129267ed8f26a597340ad7bf38b39d03f1abc38b6cbca1ffca024c36fc6785fff4cca6a89ebd052c051e9e5b5aace42caea059af6e49',
        'nurse')
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='nurse'"))
