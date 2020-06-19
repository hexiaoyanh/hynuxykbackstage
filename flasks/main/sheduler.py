import datetime
import time

from . import scheduler
from flask import current_app

from .models import Curriculum, WXUser
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
        users = WXUser.query.filter(WXUser.is_subnotice == True).all()
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
