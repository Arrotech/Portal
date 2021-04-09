from app.api.v1 import portal_v1
from flask_jwt_extended import jwt_required
from utils.authorization import admin_required
from utils.utils import check_stream_keys, raise_error
from flask import request
from app.api.v1.models.streams import StreamsModel
from utils.serializer import Serializer


@portal_v1.route('/streams', methods=['POST'])
def add_stream():
    """Add a new stream."""
    errors = check_stream_keys(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    stream_name = details['stream_name']
    if StreamsModel().get_stream_by_name(stream_name):
        return raise_error(400, '{} already exists'.format(stream_name))
    response = StreamsModel(stream_name).save()
    return Serializer.serialize(response, 201, 'Stream added successfully')


@portal_v1.route('/streams', methods=['GET'])
def get_all_streams():
    """Have a user able to view all streams."""
    response = StreamsModel().get_all_streams()
    return Serializer.serialize(response, 200, "Streams retrived successfully")


@portal_v1.route('/streams/<int:stream_id>', methods=['GET'])
def get_stream_by_id(stream_id):
    """Have a user able to view stream by id."""
    response = StreamsModel().get_stream_by_id(stream_id)
    if response:
        return Serializer.serialize(response, 200,
                                    "Stream retrived successfully")
    return raise_error(404, 'Stream not found')


@portal_v1.route('/streams/<string:stream_name>', methods=['GET'])
def get_stream_by_name(stream_name):
    """Have a user able to view stream by name."""
    response = StreamsModel().get_stream_by_name(stream_name)
    if response:
        return Serializer.serialize(response, 200,
                                    "Stream retrived successfully")
    return raise_error(404, 'Stream not found')
