#!/bin/sh

echo "Inside entrypoint"
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Remove all data from db, perhaps instead of destroying the volume
# python manage.py flush --no-input

DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --username=charlie --email=cmaunderc@gmail.com --noinput

python manage.py migrate

exec "$@"
