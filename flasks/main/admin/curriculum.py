from flask import request, jsonify
from flask_login import login_required

from . import admin
from main import admin_required
from ..models import Curriculum


@admin.route('/query_curriculum')
@login_required
@admin_required
def query_curriculum():
    pages = request.args.get('pages')
    num = request.args.get('num')
    curriculum = Curriculum.query.paginate(int(pages), int(num)).items
    data = {}
    for i in curriculum:
        data[i.id] = {
            "userid": i.userid,
            "school_year": i.school_year,
            "week": i.week,
            "class_time": i.class_time,
            "class_name": i.class_name,
            "teacher": i.teacher,
            "location": i.location,
            "begin_time": i.begintime,
            "end_time": i.endtime,
            "cycle": i.cycle
        }
    return jsonify(data)


@admin.route('/query_curriculum_by_userid')
@login_required
@admin_required
def query_curriculum_by_userid():
    pass
