#!/bin/bash

set -e

/home/www-data/app/.venv/bin/python /home/www-data/app/manage.py makemigrations
/home/www-data/app/.venv/bin/python /home/www-data/app/manage.py migrate
/home/www-data/app/.venv/bin/python /home/www-data/app/manage.py collectstatic --noinput

if [ $UID -eq 0 ]
then
    service gunicorn start
else
    sudo service gunicorn start
fi
