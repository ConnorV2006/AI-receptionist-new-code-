"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Users
    op.create_table('user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password', sa.String(200), nullable=False),
        sa.Column('role', sa.String(20), default='staff')
    )

    # Clinics
    op.create_table('clinic',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('slug', sa.String(50), unique=True),
        sa.Column('twilio_number', sa.String(20)),
        sa.Column('twilio_sid', sa.String(120)),
        sa.Column('twilio_token', sa.String(120))
    )

    # Patients
    op.create_table('patient',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('dob', sa.Date)
    )

    # Visits
    op.create_table('visit',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patient.id')),
        sa.Column('date', sa.DateTime),
        sa.Column('notes', sa.Text),
        sa.Column('summary_pdf', sa.String(200))
    )

    # Paystubs
    op.create_table('paystub',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('employee', sa.String(120)),
        sa.Column('period', sa.String(50)),
        sa.Column('gross', sa.Float),
        sa.Column('net', sa.Float)
    )

    # Appointments
    op.create_table('appointment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_name', sa.String(120)),
        sa.Column('date', sa.Date),
        sa.Column('time', sa.Time)
    )

    # Reminders
    op.create_table('reminder',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('phone', sa.String(20)),
        sa.Column('message', sa.Text),
        sa.Column('send_time', sa.DateTime)
    )

    # File Uploads
    op.create_table('file_upload',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('filename', sa.String(200)),
        sa.Column('path', sa.String(300)),
        sa.Column('uploaded_at', sa.DateTime)
    )

    # Call Logs
    op.create_table('call_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('clinic_id', sa.Integer, sa.ForeignKey('clinic.id')),
        sa.Column('from_number', sa.String(20)),
        sa.Column('to_number', sa.String(20)),
        sa.Column('status', sa.String(50)),
        sa.Column('timestamp', sa.DateTime)
    )

    # Message Logs
    op.create_table('message_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('clinic_id', sa.Integer, sa.ForeignKey('clinic.id')),
        sa.Column('from_number', sa.String(20)),
        sa.Column('to_number', sa.String(20)),
        sa.Column('body', sa.Text),
        sa.Column('timestamp', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('message_log')
    op.drop_table('call_log')
    op.drop_table('file_upload')
    op.drop_table('reminder')
    op.drop_table('appointment')
    op.drop_table('paystub')
    op.drop_table('visit')
    op.drop_table('patient')
    op.drop_table('clinic')
    op.drop_table('user')
