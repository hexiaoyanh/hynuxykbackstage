from . import scheduler
from flask import current_app

from .models import Curriculum, WXUser
from .wxfwh.sendnotification import send_class_notification
from . import nowdates


@scheduler.task('interval', seconds=10, id='eight')
def eight():
    # with scheduler.app.app_context():
    #     users = WXUser.query.filter(WXUser.is_subnotice==True).all()
    #
    pass
