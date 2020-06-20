import datetime
import time

from . import scheduler, db
from flask import current_app

from .models import Curriculum, WXUser, User, Usern
from .verifyjw import verifyjw
from .wxfwh.sendnotification import send_class_notification
from . import nowdates


def get_next_half_an_hours():
    generator_hours = int(time.strftime("%H"))
    generator_minutes = int(time.strftime("%M"))
    if generator_minutes == 0: generator_minutes = 30
    if generator_minutes == 30:
        generator_hours += 1
        generator_minutes = 0
    if generator_hours == 24: generator_hours = 0
    if generator_hours <= 9:
        generator_hours = "0" + str(generator_hours)
    else:
        generator_hours = str(generator_hours)
    if generator_minutes <= 9:
        generator_minutes = "0" + str(generator_minutes)
    else:
        generator_minutes = str(generator_minutes)
    return generator_hours + ":" + generator_minutes


@scheduler.task('interval', minutes=30, id='send_class_notification', start_date='2020-6-19 14:30:00')
def send_class_notificate():
    with scheduler.app.app_context():
        now_time = nowdates.get()
        weekday = str(datetime.datetime.now().weekday() + 1)
        # 查询订阅了且没有过期的
        users = WXUser.query.filter(WXUser.is_subnotice == True, WXUser.expires_in >= datetime.datetime.now()).all()
        for i in users:
            if not i.notification_status: continue
            data = Curriculum.query.filter(Curriculum.class_time.like(weekday + '%'),
                                           Curriculum.week == now_time['week'],
                                           Curriculum.school_year == now_time['xn'],
                                           Curriculum.userid == i.userid,
                                           Curriculum.begintime == get_next_half_an_hours()
                                           ).first()
            if data is None: continue
            send_class_notification(i.openid, data.class_name, data.location, data.teacher, data.begintime)


# @scheduler.task('interval', hours=1, id='send_exam_notification', start_date='2020-6-19 14:30:00')
# def send_exam_notification():
#     with scheduler.app.app_context():
#         now_time = nowdates.get()
#         # 处理得到下个学期的id
#         now_time['xn'] = now_time['xn'].split('-')
#         if now_time['xn'][2] == '2':
#             now_time['xn'] = str(int(now_time['xn'][0]) + 1) + '-' + str(int(now_time['xn'][1]) + 1) + '-1'
#         else:
#             now_time['xn'] = now_time['xn'][0] + '-' + now_time['xn'][1] + '-2'
#         users = WXUser.query.filter(WXUser.userid is not None).all()
#         for i in users:
#             token = verifyjw.login(i.userid, i.password)
#             exam = verifyjw.get_exam(token, i.userid, now_time['xn'])
#             user = Usern.query.get(i.userid) if i.userid[0] == 'N' else User.query.get(i.userid)
#             for j in exam:
#                 if j is None: continue
#                 print(j)
#                 row = select_data(db, i.userid, now_time['xn'], j['ksxzmc'], j['kcmc'])
#                 print(row)
#                 if row != 0:
#
#
# # 查询数据
# def select_data(mycursor, userid, xn, ksxzmc, kcmc):
#     userid = userid[:5] if userid[0] == 'N' else userid[:4]
#     sql = "select ifnull((select id  from grade_1769 where userid=(:userid) and xqmc=(:xn) and ksxzmc=(:ksxzmc) and ksxzmc=(:ksxzmc) and kcmc=(:kcmc) limit 1 ), 0)".format(
#         userid)
#     value = {"userid": userid, "xn": xn, "ksxzmc": ksxzmc, "kcmc": kcmc}
#     rows = mycursor.session.execute(sql, value).fetchall()
#     return rows
#
# def insert_data(table_name, data):
#     sql = "insert into grade_{} (userid, bz, cjbsmc, kclbmc, zcj, xm, xqmc, kcxzmc, ksxzmc, kcmc, xf, bj) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(
#         table_name)
#     value = (
#         data['userid'],
#         data['bz'],
#         data['cjbsmc'],
#         data['kclbmc'],
#         data['zcj'],
#         data['xm'],
#         data['xqmc'],
#         data['kcxzmc'],
#         data['ksxzmc'],
#         data['kcmc'],
#         data['xf'],
#         data['bj'])
#     mycursor.execute(sql, value)
#     mydb.commit()