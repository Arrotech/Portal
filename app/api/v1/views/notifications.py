import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.notifications import NotificationsModel
from app.api.v1.models.users_model import UsersModel
from utils.utils import check_notification_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import portal_v1
from app.api.v1.services.mails.mail_services import send_email


@portal_v1.route('/notifications', methods=['POST'])
@jwt_required
@admin_required
def send_notification():
    """Send new notificfation."""
    errors = check_notification_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    subject = details['subject']
    description = details['description']
    response = NotificationsModel(subject, description).save()
    users = json.loads(UsersModel().get_all_users())
    for user in users:
        email = user['email']
        send_email(subject,
                sender='arrotechdesign@gmail.com',
                recipients=[email],
                text_body=description,
                html_body=description)
    return Serializer.serialize(response, 201, "Notification sent successfully")

@portal_v1.route('/notifications/<int:notification_id>', methods=['GET'])
@jwt_required
def get_notification_by_id(notification_id):
    """Fetch institution by id."""
    response = NotificationsModel().get_notitications_by_id(notification_id)
    if response:
        return Serializer.serialize(response, 200, "Notifications retrieved successfully")
    return raise_error(404, "Notifications not found")