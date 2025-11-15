release: python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn --bind 0.0.0.0:8080 config.wsgi:application