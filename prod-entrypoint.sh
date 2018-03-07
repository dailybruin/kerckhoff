#!/bin/sh
set -e
# Build Webpack
echo "Building webpack..."
npm run build

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

exec "$@"
