import datetime
import threading

from flask import request, jsonify
from flask_login import login_required

from . import admin
from main import admin_required
from ..models import Curriculum, WXUser


@admin.route('/query_curriculum')
@login_required
@admin_required
def query_curriculum():
    pages = request.args.get('pages')
    num = request.args.get('num')
    curriculum = Curriculum.query.paginate(int(pages), int(num))
    data = []
    for i in curriculum.items:
        data.append({
            "id": i.id,
            "userid": i.userid,
            "school_year": i.school_year,
            "week": i.week,
            "class_time": i.class_time,
            "class_name": i.class_name,
            "teacher": i.teacher,
            "location": i.location,
            "begin_time": " ",
            "end_time": " ",
            "cycle": " "
        })
    return jsonify({'data': data, 'total_number': curriculum.pages})


@admin.route('/query_curriculum_by_userid')
@login_required
@admin_required
def query_curriculum_by_userid():
    userid = request.args.get('userid')
    curriculum = Curriculum.query.filter(Curriculum.userid == userid).all()
    data = []
    for i in curriculum:
        data.append({
            "id": i.id,
            "userid": i.userid,
            "school_year": i.school_year,
            "week": i.week,
            "class_time": i.class_time,
            "class_name": i.class_name,
            "teacher": i.teacher,
            "location": i.location,
            "begin_time": " ",
            "end_time": " ",
            "cycle": " "
        })
    return jsonify(data)


from .update_curriculum import Update_curriculum

update_curriculum = Update_curriculum()


# 更新所有人的课表
@admin.route('/update_class')
# @login_required
# @admin_required
def update_class():
    now_time = datetime.datetime.now()
    user = WXUser.query.filter(WXUser.server_expire >= now_time).all()
    thr = threading.Thread(target=update_curriculum.update_class, args=[user, ])  # 创建线程更新课表
    thr.start()
    return jsonify({
        "code": 1,
        "msg": "任务已接收"
    })


# 获取当前的进度
@admin.route('/get_schedule')
@login_required
@admin_required
def get_schedule():
    if update_curriculum.is_running:
        return jsonify({
            "code": 1,
            "schedule": update_curriculum.get_schedule()
        })
    else:
        return jsonify({
            "code": -1,
            "msg": "没有任务在运行"
        })
