
web: gunicorn run:app
worker: celery -A app.api.v1.services.mails.mail_services.celery worker --loglevel=info --pool=solo
