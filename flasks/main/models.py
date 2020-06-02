from sqlalchemy import Column

from . import db


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
