#!/bin/sh
set -e

cd kerckhoff

# Collect static files
echo "Collect static files"
python3.7 manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3.7 manage.py migrate

cd ..

exec "$@"
