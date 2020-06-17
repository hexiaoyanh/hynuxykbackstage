import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    threaded = True
    processes = True
    SECRET_KEY = "BU*8YVY*inNYG7JNON8TR%BR@#$VHJV"
    PERMANENT_SESSION_LIFETIME = timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:03190319@localhost:3306/grade?charset=utf8mb4"
    WECHAT_APPID = os.getenv('appid')
    WECHAT_SECRET = os.getenv('wx_qqsecret')
    WECHAT_TOKEN="mikahemikahe"
    @staticmethod
    def __int__(self):
        pass
