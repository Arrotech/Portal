import os
from celery import Celery
from app.__init__ import exam_app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker='amqps://wmznztra:2jFJ5RUUV4daZWzPWLcW5bczw2vFP2CJ@moose.rmq.cloudamqp.com/wmznztra'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
