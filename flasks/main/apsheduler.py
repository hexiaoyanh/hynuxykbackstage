import datetime

from . import scheduler
from flask import current_app

from .models import Curriculum, WXUser
from .wxfwh.sendnotification import send_class_notification
from . import nowdates


@scheduler.task('interval', minutes=1, id='send_class_notification', start_date='2020-6-19 13:54:00')
def send_class_notification():
    with scheduler.app.app_context():
        print(datetime.datetime.now())
        now_time = nowdates.get()
        weekday = str(datetime.datetime.now().weekday() + 1)
        users = WXUser.query.filter(WXUser.is_subnotice == True).all()
        for i in users:
            pass
