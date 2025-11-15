release: python manage.py collectstatic --noinput --clear && python manage.py migrate
web: python manage.py collectstatic --noinput --clear && gunicorn --bind 0.0.0.0:8080 config.wsgi:application