from flask import Blueprint

portal_v1 = Blueprint('portal_v1', __name__,
                          template_folder='../../../templates', static_folder='../../../../static')

from app.api.v1.views import exam_views, subjects_view, units,\
     auth_views, library_views, fees_views, hostels,\
     departments, courses, apply_course, accommodation, checklist, campuses, certificates, institutions, notifications