"""Add individual indexes for appointments, doctor_notes, patients, users, etc.

Revision ID: 0010_add_indexes
Revises: 0009_seed_notes
Create Date: 2025-10-03
"""
from alembic import op

# Revision identifiers, used by Alembic.
revision = "0010_add_indexes"
down_revision = "0009_seed_notes"
branch_labels = None
depends_on = None


def upgrade():
    # Appointments indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_appointments_doctor_id ON appointments (doctor_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_appointments_patient_id ON appointments (patient_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_appointments_scheduled_time ON appointments (scheduled_time);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    # Doctor notes indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_doctor_notes_doctor_id ON doctor_notes (doctor_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_doctor_notes_patient_id ON doctor_notes (patient_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_doctor_notes_created_at ON doctor_notes (created_at);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    # Patients indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_patients_last_name ON patients (last_name);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_patients_email ON patients (email);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    # Audit logs indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_audit_logs_user_id ON audit_logs (user_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_audit_logs_timestamp ON audit_logs (timestamp);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    # Nurse profiles indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_nurse_profiles_nurse_id ON nurse_profiles (nurse_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    # Users indexes
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_users_role_id ON users (role_id);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_users_created_at ON users (created_at);",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )


def downgrade():
    # Drop indexes in reverse order
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_users_created_at;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_users_role_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_nurse_profiles_nurse_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_audit_logs_timestamp;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_audit_logs_user_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_patients_email;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_patients_last_name;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_doctor_notes_created_at;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_doctor_notes_patient_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_doctor_notes_doctor_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_appointments_scheduled_time;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_appointments_patient_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_appointments_doctor_id;",
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
