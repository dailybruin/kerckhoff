#!/bin/sh
set -e

cd kerckhoff

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

cd ..

exec "$@"
