release: python manage.py db migrate
release: python manage.py db upgrade
web: gunicorn gettingstarted.wsgi --log-file -
