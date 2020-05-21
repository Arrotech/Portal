import os
from threading import Thread
from flask import make_response, jsonify, render_template
from flask_mail import Message, Mail
from app.__init__ import exam_app as my_app
from utils.utils import raise_error
from app.api.v1 import auth_v1
from app.config import app_config

config_name = os.getenv('APP_SETTINGS')
app = my_app(config_name)
app.config.from_pyfile('config.py')
app.config["SECRET_KEY"] = 'schoolportal'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
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
