import os
from celery import Celery
from config import app_config

config_name = os.environ.get('FLASK_ENV')


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app_config[config_name].RABBITMQ_URL
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
