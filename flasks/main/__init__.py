from flask import Flask

from .query import query

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from .nowdate import nowdate
from .get_access_token import get_access_token

access_token = get_access_token()

from .settings import WechatSetting

#wechatsettings = WechatSetting()

db = SQLAlchemy()
login_manager = LoginManager()
nowdates = nowdate(2020, 2, 17)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)

    #wechatsettings.init_app(app)

    from .query import query as query_blueprint
    app.register_blueprint(query_blueprint, url_prefix='/query')

    from .publicexam import publicexam as publicexam_blueprint
    app.register_blueprint(publicexam_blueprint, url_prefix='/publicexam')

    from .submsg import submsg as submsg_blueprint
    app.register_blueprint(submsg_blueprint, url_prefix='/submsg')

    from .rank import rank as rank_blueprint
    app.register_blueprint(rank_blueprint, url_prefix='/rank')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .wxfwh import wxfwh as wxfwh_blueprint
    app.register_blueprint(wxfwh_blueprint, url_prefix='/wxfwh')

    return app
