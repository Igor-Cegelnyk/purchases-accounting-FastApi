#!/bin/bash
set -e

echo "Run apply migrations.."
cd /app/backend
poetry run alembic upgrade head
echo "Migrations applied!"

echo "Generating keys..."
bash /app/backend/generate_keys.sh

cd /app
exec poetry run uvicorn backend.main:main_app --host "$APP_CONFIG__RUN__HOST" --port "$APP_CONFIG__RUN__PORT"
