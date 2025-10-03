#!/usr/bin/env bash
set -e

echo "🔄 Resetting database + seeding demo data..."

# Drop all tables
echo "❌ Dropping all tables..."
psql "$DATABASE_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Run migrations
echo "📦 Applying migrations..."
flask db upgrade

# Seed demo data
echo "🌱 Seeding demo data..."
python seed.py

echo "✅ Database reset + demo seed completed successfully."
