"""Seed admin and superadmin"""

from alembic import op
import sqlalchemy as sa

revision = "0002_seed_roles"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute(sa.text("""
        INSERT INTO "user" (username, email, password, role)
        VALUES 
        ('admin', 'admin@example.com',
        'scrypt:32768:8:1$7kYyX6wtCa3ZvBpf$df5b36e3ee6a652b4c59042f902ce13d9b2f03206e106e284c7b1f1ae1809c2987431825dddd7e86728aa4642efa69beaf7dbfda0b6d0ef48f63dc485796cade',
        'admin'),

        ('superadmin', 'superadmin@example.com',
        'scrypt:32768:8:1$bpF9vHR8N65IsucX$eb7654d1672173d859e690b6199dda4183fce37f4b17dc96223a10ddfbaaf49307bb34897e718d3dee3998b98616b69cc55f17a351682ba69ddae869f4435224',
        'superadmin')
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role IN ('admin','superadmin')"))
