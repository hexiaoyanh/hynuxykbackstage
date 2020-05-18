from flask import Blueprint, Flask

from config import Config
from main.query import query

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from .query import query as query_blueprint
    app.register_blueprint(query_blueprint, url_prefix='/query')

    from .publicexam import publicexam as publicexam_blueprint
    app.register_blueprint(publicexam_blueprint, url_prefix='/publicexam')

    from .submsg import submsg as submsg_blueprint
    app.register_blueprint(submsg_blueprint, url_prefix='/submsg')

    from .rank import rank as rank_blueprint
    app.register_blueprint(rank_blueprint, url_prefix='/rank')

    return app
