"""Add nurse table and seed sample nurse"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '0007_add_nurse_table'
down_revision = '0006_seed_demo_data'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'nurse',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('clinic_id', sa.Integer(), sa.ForeignKey('clinic.id'), nullable=False),
    )

    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO nurse (name, email, clinic_id)
        VALUES ('Emily Carter', 'emily.carter@example.com', 1)
    """))

def downgrade():
    op.drop_table('nurse')
