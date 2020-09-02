import datetime

from flask import request, jsonify
from flask_login import login_required

from . import admin

# 设置开学日期
from main import admin_required, nowdates, wechatsettings, db
from ..models import User, Usern, Grade, WXUser, Keywords
from ..wxfwh.sendnotification import send_start_school_notifications


@admin.route('/set_time')
@login_required
@admin_required
def set_time():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    nowdates.set(int(year), int(month), int(day))
    return jsonify({
        "code": 1,
        "msg": "开学日期设置成功"
    })


@admin.route('/get_begin_time')
@login_required
@admin_required
def get_begin_time():
    return jsonify(nowdates.get_begin_time())


# 获取开学日期
@admin.route('/get_time')
@login_required
@admin_required
def get_time():
    return nowdates.get()


@admin.route('/get_customize_menu')
@login_required
@admin_required
def get_customize_menu():
    return wechatsettings.get_menu()


@admin.route('/set_customize_menu', methods=['POST'])
@login_required
@admin_required
def set_customize_menu():
    data = str(request.data, 'utf-8')
    wechatsettings.set_menu(data)
    return jsonify({
        "code": 1,
        "msg": "ok"
    })


@admin.route('/get_total_fee')
@login_required
@admin_required
def get_total_fee():
    return jsonify({
        "code": 1,
        "total_fee": wechatsettings.get_total_fee()
    })


@admin.route('/set_total_fee')
@login_required
@admin_required
def set_total_fee():
    total_fee = request.args.get('total_fee')
    wechatsettings.set_total_fee(total_fee)
    return jsonify({
        "code": 1,
        "msg": "设置成功"
    })


@admin.route('/send_start_school_notifications', methods=['POST'])
@login_required
@admin_required
def send_school_notifications():
    data = request.get_json()
    # user = WXUser.query.all()
    send_start_school_notifications("ovtKGs1iMFFTTClFSQtRmfqsIkt0", data['time_msg'], data['remark_msg'], data['url'])
    # for i in user:
    #     send_start_school_notifications(i.openid, data['time_msg'], data['remark_msg'], data['url'])
    return jsonify({
        "code": 1,
        "msg": "任务已添加"
    })


rank2grade = {
    "优": 95,
    "良": 85,
    "中": 75,
    "及格": 60,
    "合格": 60,
    "不及格": 0,
    '不通过': 0,
    "通过": 60
}


# 判断是否含中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# 获取排名
def getrank(people, userid, obj):
    people = sorted(people, key=lambda x: float(x[obj]), reverse=True)
    print(people)
    rank = 1
    for i in people:
        if i['xh'] == userid: break
        rank += 1
    return rank


# 给所有人添加福利的方法
@admin.route('/fuli')
@login_required
@admin_required
def fuli():
    days = request.args.get('days')
    user = WXUser.query.all()
    for i in user:
        # 体验版和过期用户
        print(i.expires_in)
        if i.server_expire is None or i.server_expire <= datetime.datetime.now() :
            i.is_experience = True
            i.server_expire = datetime.datetime.now() + datetime.timedelta(days=int(days))
        else:
            i.server_expire += datetime.timedelta(days=int(days))

        db.session.add(i)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "福利添加成功"
    })

# @admin.route('/generate_data_analysis')
# # @login_required
# # @admin_required
# def generate_data_analysis():
#     grade_distributed = {}  # 成绩分布
#     gpa_rank = {}  # 北大GPA排名
#     ave_gpa_rank = {}  # 平均学分绩点排名
#     class_gpa_rank = {}  # 班级平均gpa排名
#     class_ave_gpa_rank = {}  # 班级平均学分绩排名
#     # total_grade = 0  # 所有人一共考试了多少门课
#     # total_guake = 0  # 有多少门课被挂科了
#     total_eight = 0  # 有多少人平均成绩在80以上
#
#     class_flag = {}  # 所有班级
#     all_user = User.query.all()
#     all_user += Usern.query.all()
#     for user in all_user:
#         print(user.xh,user.xm)
#         class_flag[user.bj] = True
#         grade = Grade.query.filter(Grade.userid == user.xh).all()
#         total_num = 0  # 总分
#         total_credit = 0  # 总学分
#         total_pku_gpa = 0  # 北大gpa
#         total_ave_gpa = 0  # 平均学分绩点
#         for j in grade:
#             global num
#             if is_contains_chinese(j.zcj):
#                 num = rank2grade[j.zcj]
#             else:
#                 num = float(j.zcj)
#             try:
#                 grade_distributed[str(num)] += 1
#             except KeyError:
#                 grade_distributed[str(num)] = 1
#
#             total_num += num
#             if num >= 60:
#                 total_pku_gpa += (4 - 3 * (100 - num) ** 2 / 1600.0) * float(j.xf)
#             # print(j[6], j[11], float(j[11]))
#             total_credit += float(j.xf)
#             total_ave_gpa += num * float(j.xf)
#         # 北京大学gpa计算
#         total_pku_gpa = total_pku_gpa / total_credit if total_credit != 0 else 0
#         total_ave_gpa = total_ave_gpa / total_credit if total_credit != 0 else 0
#         gpa_rank[user.xh] = {
#             "xm": user.xm,
#             "bj": user.bj,
#             "pku_gpa": round(total_pku_gpa, 2)
#         }
#         ave_gpa_rank[user.xh] = {
#             "xm": user.xm,
#             "bj": user.bj,
#             "ave": round(total_ave_gpa, 2)
#         }
#         if round(total_num / len(grade) if len(grade) != 0 else 0, 2) >= 80: total_eight += 1
#     for a, b in class_flag.items():
#         if a[0] == 'N':
#             class_user = Usern.query.filter(Usern.bj == a).all()
#         else:
#             class_user = User.query.filter(Usern.bj == a).all()
#         total_gpa = 0
#         total_ave = 0
#         for i in class_user:
#             total_gpa += gpa_rank[i.xh]['pku_gpa']
#             total_ave += ave_gpa_rank[i.xh]['ave']
#         class_ave_gpa_rank[a] = round(total_gpa / len(class_user), 2)
#         class_gpa_rank[a] = round(total_ave / len(class_user), 2)
#     grade_distributed = sorted(grade_distributed.items(), key=lambda grade_distributed: grade_distributed[0],
#                                reverse=True)
#     print(dict(grade_distributed))
#     gpa_rank = sorted(gpa_rank.items(), key=lambda gpa_rank: gpa_rank[1]['pku_gpa'], reverse=True)
#     print(gpa_rank)
#     ave_gpa_rank = sorted(ave_gpa_rank.items(), key=lambda ave_gpa_rank: ave_gpa_rank[1]['ave'], reverse=True)
#
#     print(ave_gpa_rank)
#
#     class_ave_gpa_rank = sorted(class_ave_gpa_rank.items(), key=lambda class_ave_gpa_rank: class_ave_gpa_rank[1],
#                                 reverse=True)
#     print(class_ave_gpa_rank)
#
#     class_gpa_rank = sorted(class_gpa_rank.items(), key=lambda class_gpa_rank: class_gpa_rank[1], reverse=True)
#     print(class_gpa_rank)
#     return jsonify({
#         "grade_distributed": dict(grade_distributed),
#         "gpa_rank": gpa_rank
#     })
