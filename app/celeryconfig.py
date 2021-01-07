import os
from celery import Celery
from app.__init__ import exam_app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.environ.get('RABBITMQ_URL')
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
