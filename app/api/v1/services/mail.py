from threading import Thread
from flask_mail import Message
from run import app
from arrotechtools import raise_error
from app.celery import make_celery
from app import mail

celery = make_celery(app)


def send_async_email(app, msg):
    """Send asychronous email."""
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            return raise_error(500, 'Mail server not working')


@celery.task(name='mail_services.send_email')
def send_email(subject, sender, recipients, text_body, html_body):
    """Message body."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
