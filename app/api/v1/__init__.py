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

departments_v1 = Blueprint('departments_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')
courses_v1 = Blueprint('courses_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')

apply_course_v1 = Blueprint('apply_course_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')

accommodation_v1 = Blueprint('accommodation_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')

checklist_v1 = Blueprint('checklist_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')

campuses_v1 = Blueprint('campuses_v1', __name__, 
                           template_folder='../../../templates', static_folder='../../../../static')


from app.api.v1.views import exam_views, subjects_view, units, staff,\
     accountant, auth_views, library_views, fees_views, hostels,\
     departments, courses, apply_course, accommodation, checklist, campuses