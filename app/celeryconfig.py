import os
from celery import Celery
from app.__init__ import exam_app

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://redistogo:e321b5418c64a7495955088ac41a8a1b@pike.redistogo.com:11205/"
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

