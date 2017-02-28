web: python manage.py collectstatic --noinput; gunicorn smarttools.wsgi --log-file -
worker: celery worker --app=smarttools