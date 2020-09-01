import datetime
import time

import requests

from . import scheduler, db
from flask import current_app

from .models import Curriculum, WXUser, User, Usern, Grade, Keywords
from .verifyjw import verifyjw
from .wxfwh.sendnotification import send_class_notification, send_exam_notification, send_ad_notification
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
        print("----------------------上课提醒开始：")
        now_time = nowdates.get()
        weekday = str(datetime.datetime.now().weekday() + 1)
        # 查询订阅了且没有过期的
        users = WXUser.query.filter(WXUser.is_subnotice == True, WXUser.server_expire >= datetime.datetime.now()).all()
        sub_text = Keywords.query.filter(Keywords.keyword == 'class_sub_text').first().reply
        not_sub_text = Keywords.query.filter(Keywords.keyword == 'class_not_sub_text').first().reply
        for i in users:
            if not i.notification_status: continue
            data = Curriculum.query.filter(Curriculum.class_time.like(weekday + '%'),
                                           Curriculum.week == now_time['week'],
                                           Curriculum.school_year == now_time['xn'],
                                           Curriculum.userid == i.userid,
                                           Curriculum.begintime == get_next_half_an_hours()
                                           ).first()
            if data is None: continue
            if i.is_experience:
                send_class_notification(i.openid, data.class_name, data.location, data.teacher, data.begintime,
                                        remark=not_sub_text)
            else:
                send_class_notification(i.openid, data.class_name, data.location, data.teacher, data.begintime,
                                        remark=sub_text)

        print("----------------------上课提醒结束")


@scheduler.task('interval', days=1, id='send_exam_notification_scheduler', start_date='2020-6-19 12:00:00')
def send_exam_notification_scheduler():
    with scheduler.app.app_context():
        print("----------------------考试成绩开始")
        now_time = nowdates.get()
        users = WXUser.query.all()
        for i in users:
            if i.userid is None or i.userid == "":
                continue
            try:
                exam = verifyjw.get_exam("token", i.userid, now_time['xn'])
            except requests.exceptions.ConnectTimeout:
                continue
            user = Usern.query.get(i.userid) if i.userid[0] == 'N' else User.query.get(i.userid)
            if user is None:
                send_ad_notification(i.userid, "没有这个学号")
                continue
            for j in exam:
                if j is None: continue
                grade = Grade.query.filter(Grade.userid == i.userid, Grade.xqmc == now_time['xn'],
                                           Grade.ksxzmc == j['ksxzmc'], Grade.kcmc == j['kcmc']).first()
                if grade is None:
                    grade = Grade(userid=i.userid, bz=j['bz'], cjbsmc=j['cjbsmc'], kclbmc=j['kclbmc'], zcj=j['zcj'],
                                  xm=user.xm, xqmc=j['xqmc'], kcxzmc=j['kcxzmc'], ksxzmc=j['ksxzmc'], kcmc=j['kcmc'],
                                  xf=j['xf'], bj=user.bj)
                    db.session.add(grade)
                    db.session.commit()
                    send_exam_notification(i.openid, j['kcmc'], j['zcj'])
        print("----------------------考试成绩结束")


@scheduler.task('interval', days=30, id='update_all_exam_score', start_date='2020-6-25 00:00:00')
def update_all_exam_score():
    with scheduler.app.app_context():
        print("----------------------所有成绩开始")
        now_time = nowdates.get()
        users = User.query.all()
        for i in users:
            try:
                exam = verifyjw.get_exam("", i.xh, now_time['xn'])
            except requests.exceptions.ConnectTimeout:
                continue
            for j in exam:
                if j is None: continue
                grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == now_time['xn'],
                                           Grade.ksxzmc == j['ksxzmc'], Grade.kcmc == j['kcmc']).first()
                if grade is None:
                    grade = Grade(userid=i.xh, bz=j['bz'], cjbsmc=j['cjbsmc'], kclbmc=j['kclbmc'], zcj=j['zcj'],
                                  xm=i.xm, xqmc=j['xqmc'], kcxzmc=j['kcxzmc'], ksxzmc=j['ksxzmc'], kcmc=j['kcmc'],
                                  xf=j['xf'], bj=i.bj)
                    db.session.add(grade)
                    db.session.commit()
        users = Usern.query.all()
        for i in users:
            try:
                exam = verifyjw.get_exam("token", i.xh, now_time['xn'])
            except requests.exceptions.ConnectTimeout:
                continue
            for j in exam:
                if j is None: continue
                grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == now_time['xn'],
                                           Grade.ksxzmc == j['ksxzmc'], Grade.kcmc == j['kcmc']).first()
                if grade is None:
                    grade = Grade(userid=i.xh, bz=j['bz'], cjbsmc=j['cjbsmc'], kclbmc=j['kclbmc'], zcj=j['zcj'],
                                  xm=i.xm, xqmc=j['xqmc'], kcxzmc=j['kcxzmc'], ksxzmc=j['ksxzmc'], kcmc=j['kcmc'],
                                  xf=j['xf'], bj=i.bj)
                    db.session.add(grade)
                    db.session.commit()
        print("----------------------所有成绩结束")
# # 查询数据
# def select_data(mycursor, userid, xn, ksxzmc, kcmc):
#     sql = "select ifnull((select id  from grade_{} where userid=(:userid) and xqmc=(:xn) and ksxzmc=(:ksxzmc) and ksxzmc=(:ksxzmc) and kcmc=(:kcmc) limit 1 ), 0)".format(
#         userid[:5] if userid[0] == 'N' else userid[:4])
#     value = {"userid": userid, "xn": xn, "ksxzmc": ksxzmc, "kcmc": kcmc}
#     rows = mycursor.session.execute(sql, value).fetchall()
#     return rows
#
#
# def insert_data(mycursor, table_name, data):
#     sql = "insert into grade_{} (userid, bz, cjbsmc, kclbmc, zcj, xm, xqmc,kcxzmc, ksxzmc,kcmc, xf, bj) values ( (:userid),(:bz),(:cjbsmc),(:kclbmc),(:zcj),(:xm),(:xqmc),(:kcxzmc),(:ksxzmc),(:kcmc),(:xf),(:bj) )".format(
#         table_name)
#     value = {
#         "userid": data['userid'],
#         "bz": data['bz'],
#         "cjbsmc": data['cjbsmc'],
#         "kclbmc": data['kclbmc'],
#         "zcj": data['zcj'],
#         "xm": data['xm'],
#         "xqmc": data['xqmc'],
#         "kcxzmc": data['kcxzmc'],
#         "ksxzmc": data['ksxzmc'],
#         "kcmc": data['kcmc'],
#         "xf": data['xf'],
#         "bj": data['bj']}
#     mycursor.session.execute(sql, value)
#     mycursor.session.commit()
