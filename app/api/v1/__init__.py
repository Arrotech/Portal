from flask import Blueprint

accountant_v1 = Blueprint('accountant_v1', __name__,
                          template_folder='../../../templates', static_folder='../../../../static')

auth_v1 = Blueprint('auth_v1', __name__,
                    template_folder='../../../templates', static_folder='../../../../static')

books_v1 = Blueprint('books_v1', __name__,
                     template_folder='../../../templates', static_folder='../../../../static')

fees_v1 = Blueprint('fees_v1', __name__,
                    template_folder='../../../templates', static_folder='../../../../static')

staff_v1 = Blueprint('staff_v1', __name__,
                     template_folder='../../../templates', static_folder='../../../../static')

units_blueprint_v1 = Blueprint('units_blueprint_v1', __name__,
                               template_folder='../../../templates', static_folder='../../../../static')
subjects_v1 = Blueprint('subjects_v1', __name__,
                        template_folder='../../../templates', static_folder='../../../../static')

exams_v1 = Blueprint('exams_v1', __name__,
                     template_folder='../../../templates', static_folder='../../../../static')

hostels_v1 = Blueprint('hostels_v1', __name__,
                     template_folder='../../../templates', static_folder='../../../../static')


from app.api.v1.views import exam_views
from app.api.v1.views import subjects_view
from app.api.v1.views import units
from app.api.v1.views import staff
from app.api.v1.views import accountant
from app.api.v1.views import auth_views
from app.api.v1.views import library_views
from app.api.v1.views import fees_views
from app.api.v1.views import hostels