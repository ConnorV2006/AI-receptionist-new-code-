"""Initial database schema

Revision ID: 0001_initial
Revises: None
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('description', sa.String(255))
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'clinics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), unique=True, nullable=False),
    )

    op.create_table(
        'patients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('phone', sa.String(20)),
        sa.Column('email', sa.String(120)),
        sa.Column('clinic_id', sa.Integer, sa.ForeignKey('clinics.id'))
    )

    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('specialty', sa.String(100))
    )

    op.create_table(
        'nurses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )

    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patients.id')),
        sa.Column('doctor_id', sa.Integer, sa.ForeignKey('doctors.id')),
        sa.Column('scheduled_time', sa.DateTime, nullable=False),
        sa.Column('notes', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
        sa.Column('details', sa.Text)
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('appointments')
    op.drop_table('nurses')
    op.drop_table('doctors')
    op.drop_table('patients')
    op.drop_table('clinics')
    op.drop_table('users')
    op.drop_table('roles')
