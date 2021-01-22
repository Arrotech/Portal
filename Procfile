
web: gunicorn run:app
worker: celery -A app.api.v1.services.mail.celery worker --loglevel=info --pool=solo
