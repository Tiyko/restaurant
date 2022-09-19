web: gunicorn appname.wsgi:luigis_castle_pizza --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate