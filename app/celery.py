import os
from celery import Celery
from instance.config import app_config


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.environ.get('REDISTOGO_URL', 'LOCAL_REDISTOGO_URL')
    )
    celery.conf.update(app_config[os.environ.get(
        'FLASK_ENV', 'development')].CELERY_CONFIG)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
