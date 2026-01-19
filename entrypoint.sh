#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is ready!"

# Run migrations
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Load sample data if database is empty
echo "Checking for sample data..."
python manage.py shell << EOF
from hotels.models import Hotel
if Hotel.objects.count() == 0:
    print('Loading sample data...')
    import os
    os.system('python manage.py load_sample_data')
else:
    print('Sample data already exists, skipping...')
EOF

echo "Starting server..."
exec "$@"
