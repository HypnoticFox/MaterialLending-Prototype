#! /usr/bin/env bash

echo "prestart.sh: Starting database migrations"
python manage.py migrate --no-input

echo "prestart.sh: Creating caching table if needed"
python manage.py createcachetable

echo "prestart.sh: Creating superuser if needed"
python manage.py shell -c "
from django.contrib.auth import get_user_model; 
User = get_user_model(); 
if not User.objects.filter(is_superuser=True).exists(): 
    User.objects.create_superuser('admin', 'admin@example.com', 'admin');
"

if [ "$PROJECT_ENVIRONMENT" = "prod" ]
then
    echo "prestart.sh: (PRODUCTION_MODE) Starting staticfiles collecting"
    python manage.py collectstatic --no-input
else
    echo "prestart.sh: (DEVELOPMENT_MODE) Adding some seed data"
    python manage.py shell -c "
from django.contrib.auth.models import Group;
if not Group.objects.filter(name='example').exists():
    Group.objects.create(name='example');
    "
fi