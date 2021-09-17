release: python manage.py migrate
web: daphne project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A project.celery worker -l info 
celerybeat: celery -A project beat -l INFO 
celeryworker2: celery -A project.celery worker & celery -A project beat -l INFO  & wait -n 