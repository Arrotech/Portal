import os
from threading import Thread
from flask import make_response, jsonify, render_template
from flask_mail import Message, Mail
from app.__init__ import exam_app as my_app
from utils.utils import raise_error
from app.api.v1 import auth_v1

config_name = os.getenv('APP_SETTINGS')
app = my_app(config_name)
mail = Mail(app)


def send_async_email(app, msg):
    """Send asychronous email."""
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            return raise_error(500, 'Mail server not working')


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
