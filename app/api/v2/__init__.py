from flask import Blueprint

portal_v2 = Blueprint('portal_v2', __name__,
                      template_folder='../../../templates', static_folder='../../../../static')

from app.api.v2.views import users  # noqa
