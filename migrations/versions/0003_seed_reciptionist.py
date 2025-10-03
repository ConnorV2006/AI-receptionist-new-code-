"""Seed receptionist"""

from alembic import op
import sqlalchemy as sa

revision = "0003_seed_receptionist"
down_revision = "0002_seed_roles"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO "user" (username, email, password, role)
        VALUES ('reception1', 'reception1@example.com',
        'scrypt:32768:8:1$01NbZGkzRUuUt1v3$09478601114007e5c2b33ad5d30fef52eeecfc75e779f8417fd934854fd3120defb5a480f365a9e684d640e6d6c746c7e893e24eb58d5019e81dd433915f1e1d',
        'receptionist')
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='receptionist'"))
