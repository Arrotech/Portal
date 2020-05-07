from flask import Blueprint

units_blueprint_v1 = Blueprint('units_blueprint_v1', __name__, template_folder='../../../templates', static_folder='../../../../static')

from app.api.v1.views import units