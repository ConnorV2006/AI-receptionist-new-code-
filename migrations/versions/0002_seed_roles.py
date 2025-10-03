"""Seed default roles

Revision ID: 0002_seed_roles
Revises: 0001_initial
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa


revision = '0002_seed_roles'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    roles_table = sa.table('roles',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('description', sa.String)
    )
    op.bulk_insert(roles_table, [
        {"name": "Admin", "description": "System Administrator"},
        {"name": "Receptionist", "description": "Front desk staff"},
        {"name": "Doctor", "description": "Medical doctor"},
        {"name": "Nurse", "description": "Nursing staff"},
    ])


def downgrade():
    op.execute("DELETE FROM roles WHERE name IN ('Admin', 'Receptionist', 'Doctor', 'Nurse')")
