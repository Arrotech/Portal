from flask import Blueprint

units_blueprint_v1 = Blueprint('units_blueprint_v1', __name__,
                               template_folder='../../../templates', static_folder='../../../../static')
subjects_v1 = Blueprint('subjects_v1', __name__,
                        template_folder='../../../templates', static_folder='../../../../static')

exams_v1 = Blueprint('exams_v1', __name__,
                        template_folder='../../../templates', static_folder='../../../../static')

from app.api.v1.views import units
from app.api.v1.views import subjects_view
from app.api.v1.views import exam_views