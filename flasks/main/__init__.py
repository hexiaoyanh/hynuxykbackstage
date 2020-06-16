from flask import Blueprint, Flask

from .query import query

from flask_sqlalchemy import SQLAlchemy

from .wxfwh.access_token import get_access_token
from config import Config

db = SQLAlchemy()
access_token = get_access_token()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    access_token.init_app(app)
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
