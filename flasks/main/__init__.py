from functools import wraps

from celery import Celery
from flask import Flask, abort

from celery_config import broker_url
from .query import query

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config
from .nowdate import nowdate

from .get_access_token import get_access_token

access_token = get_access_token()

from .settings import WechatSetting
from flask_apscheduler import APScheduler


wechatsettings = WechatSetting()
scheduler = APScheduler()
db = SQLAlchemy()
login_manager = LoginManager()
nowdates = nowdate(2020, 2, 17)
celery = Celery(__name__, broker=broker_url)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)
    nowdates.init_app(app)
    wechatsettings.init_app(app)
    # 初始化备份数据库定时器
    scheduler.init_app(app)
    from . import sheduler
    scheduler.start()

    # 注册celery
    register_celery(app)
    from .query import query as query_blueprint
    app.register_blueprint(query_blueprint, url_prefix='/query')

    from .publicexam import publicexam as publicexam_blueprint
    app.register_blueprint(publicexam_blueprint, url_prefix='/publicexam')

    from .rank import rank as rank_blueprint
    app.register_blueprint(rank_blueprint, url_prefix='/rank')

    from .wxfwh import wxfwh as wxfwh_blueprint
    app.register_blueprint(wxfwh_blueprint, url_prefix='/wxfwh')

    from main.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .donate import donate as donate_blueprint
    app.register_blueprint(donate_blueprint, url_prefix='/donate')

    return app


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(401)

    return decorated_view


def register_celery(app):
    celery.config_from_object('celery_config')

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
