"""
seed.py

⚠️ NOTE:
Seeding is now fully handled inside Alembic migrations.
This script is intentionally a no-op to avoid reseeding data
and causing conflicts during deployment.
"""

def run_seed():
    print("⚠️ Skipping seed: all demo data is applied via migrations.")

if __name__ == "__main__":
    run_seed()
