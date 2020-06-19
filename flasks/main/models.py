import datetime

from flask_login import UserMixin
from sqlalchemy import Column

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return WXUser.query.get(int(user_id))


# 定义User对象:
class User(db.Model):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    xh = Column(db.String(64), primary_key=True)  # 学号
    xm = Column(db.String(64))  # 姓名
    fxzy = Column(db.String(64))  # 辅修专业
    usertype = Column(db.String(64))  # 用户类型
    yxmc = Column(db.String(64))  # 学院名称
    xz = Column(db.String(64))  # 学制
    bj = Column(db.String(64))  # 班级
    dh = Column(db.String(64))  # 电话
    email = Column(db.String(64))  # 邮箱
    rxnf = Column(db.String(64))  # 入学年份
    ksh = Column(db.String(64))  # 高考学号
    nj = Column(db.String(64))  # 年级
    qq = Column(db.String(64))
    zymc = Column(db.String(64))  # 专业名称

    def __repr__(self):
        return "<User " + self.xh + " " + self.xm + " " + self.yxmc + " " + self.zymc + ">"


class Usern(db.Model):
    # 表的名字:
    __tablename__ = 'usern'

    # 表的结构:
    xh = Column(db.String(64), primary_key=True)  # 学号
    xm = Column(db.String(64))  # 姓名
    fxzy = Column(db.String(64))  # 辅修专业
    usertype = Column(db.String(64))  # 用户类型
    yxmc = Column(db.String(64))  # 学院名称
    xz = Column(db.String(64))  # 学制
    bj = Column(db.String(64))  # 班级
    dh = Column(db.String(64))  # 电话
    email = Column(db.String(64))  # 邮箱
    rxnf = Column(db.String(64))  # 入学年份
    ksh = Column(db.String(64))  # 高考学号
    nj = Column(db.String(64))  # 年级
    qq = Column(db.String(64))
    zymc = Column(db.String(64))  # 专业名称
    xb = Column(db.String(64))
    dqszj = Column(db.String(64))

    def __repr__(self):
        return "<Usern " + self.xh + " " + self.xm + " " + self.yxmc + " " + self.zymc + ">"


class WXUser(db.Model, UserMixin):
    __tablename__ = 'wxuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(12), index=True)
    password = db.Column(db.String(20))
    openid = db.Column(db.String(128), index=True)
    nicename = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    province = db.Column(db.String(12))
    city = db.Column(db.String(12))
    country = db.Column(db.String(12))
    headimgurl = db.Column(db.String(1024))
    access_token = db.Column(db.String(128))
    expires_in = db.Column(db.DateTime, default=datetime.datetime.now())
    refresh_token = db.Column(db.String(128))
    server_expire = db.Column(db.DateTime)
    is_subnotice = db.Column(db.Boolean, default=False)


class Curriculum(db.Model):
    __tablename__ = 'curriculum'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(12), index=True)
    school_year = db.Column(db.String(32), index=True)
    week = db.Column(db.Integer, index=True)
    class_time = db.Column(db.String(16), index=True)
    class_name = db.Column(db.String(16))
    teacher = db.Column(db.String(32))
    location = db.Column(db.String(32))
    begintime = db.Column(db.String(16),index=True)
    endtime = db.Column(db.String(16))
    cycle = db.Column(db.String(64))


class Bill(db.Model):
    __tablename__ = 'bill'
    transaction_id = db.Column(db.String(32), primary_key=True, index=True)  # 微信支付单号
    out_trade_no = db.Column(db.String(32), index=True)  # 商户订单号
    total_fee = db.Column(db.Integer)
    result_code = db.Column(db.String(16))
    openid = db.Column(db.String(128))
