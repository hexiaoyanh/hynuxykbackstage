# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, create_engine, Table, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, backref, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# user_grade = Table('user_grade',
#                    Base.metadata,
#                    Column('user_xh', String(20), ForeignKey('user.xh'), primary_key=True),
#                    Column('grade_kcmc', String(20), ForeignKey('grade.id'), primary_key=True)
#                    )


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    xh = Column(String(64), primary_key=True)  # 学号
    bj = Column(String(64))  # 班级
    xm = Column(String(64))  # 姓名
    fxzy = Column(String(64))  # 辅修专业
    usertype = Column(String(64))  # 用户类型
    yxmc = Column(String(64))  # 学院名称
    xz = Column(String(64))  # 学制
    dh = Column(String(64))  # 电话
    email = Column(String(64))  # 邮箱
    rxnf = Column(String(64))  # 入学年份
    ksh = Column(String(64))  # 高考学号
    nj = Column(String(64))  # 年级
    qq = Column(String(64))
    zymc = Column(String(64))  # 专业名称

    dayi_shang_num = Column(String(64))  # 大一上总分
    dayi_xia_num = Column(String(64))  # 大一下总分
    daer_shang_num = Column(String(64))
    daer_xia_num = Column(String(64))
    dasan_shang_num = Column(String(64))
    dasan_xia_num = Column(String(64))
    dasi_shang_num = Column(String(64))
    dasi_xia_num = Column(String(64))

    dayi_shang_ave = Column(String(64))  # 大上一平均分
    dayi_xia_ave = Column(String(64))  # 大一下平均分
    daer_shang_ave = Column(String(64))
    daer_xia_ave = Column(String(64))
    dasan_shang_ave = Column(String(64))
    dasan_xia_ave = Column(String(64))
    dasi_shang_ave = Column(String(64))
    dasi_xia_ave = Column(String(64))

    dayi_shang_gpa = Column(String(64))  # 大一上gpa
    daer_shang_gpa = Column(String(64))
    dasan_shang_gpa = Column(String(64))
    dasi_shang_gpa = Column(String(64))
    dayi_xia_gpa = Column(String(64))
    daer_xia_gpa = Column(String(64))
    dasan_xia_gpa = Column(String(64))
    dasi_xia_gpa = Column(String(64))

    dayi_shang_xf = Column(String(64))  # 大一上学分
    dayi_xia_xf = Column(String(64))
    daer_shang_xf = Column(String(64))
    daer_xia_xf = Column(String(64))
    dasan_shang_xf = Column(String(64))
    dasan_xia_xf = Column(String(64))
    dasi_shang_xf = Column(String(64))
    dasi_xia_xf = Column(String(64))

    # grade = relationship('grade', secondary=user_grade, backref=backref('grade'))
    def __repr__(self):
        return "<User " + self.xh + " " + self.xm + " " + self.yxmc + " " + self.zymc + ">"


#
# class Grade(Base):
#     __tablename__ = 'grade'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     userid = Column(String(64))  # 学号
#     bz = Column(String(64))  # 未知
#     cjbsmc = Column(String(64))  # 特殊情况通报，例如“作弊”“缺考”
#     kclbmc = Column(String(64))  # 课程类别名称
#     zcj = Column(String(64))  # 总成绩
#     xm = Column(String(64))  # 学生姓名
#     xqmc = Column(String(64))  # 学期名称
#     kcxzmc = Column(String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
#     ksxzmc = Column(
#         String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
#     kcmc = Column(String(64))  # 课程名称
#     xf = Column(String(10))  # 学分
#     bj = Column(String(64))


class yiliu(Base):
    __tablename__ = 'yiliu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(64))  # 学号
    bz = Column(String(64))  # 未知
    cjbsmc = Column(String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(String(64))  # 课程类别名称
    zcj = Column(String(64))  # 总成绩
    xm = Column(String(64))  # 学生姓名
    xqmc = Column(String(64))  # 学期名称
    kcxzmc = Column(String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(String(64))  # 课程名称
    xf = Column(String(10))  # 学分
    bj = Column(String(64))  # 班级


class yiqi(Base):
    __tablename__ = 'yiqi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(64))  # 学号
    bz = Column(String(64))  # 未知
    cjbsmc = Column(String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(String(64))  # 课程类别名称
    zcj = Column(String(64))  # 总成绩
    xm = Column(String(64))  # 学生姓名
    xqmc = Column(String(64))  # 学期名称
    kcxzmc = Column(String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(String(64))  # 课程名称
    xf = Column(String(10))  # 学分
    bj = Column(String(64))  # 班级


class yiba(Base):
    __tablename__ = 'yiba'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(64))  # 学号
    bz = Column(String(64))  # 未知
    cjbsmc = Column(String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(String(64))  # 课程类别名称
    zcj = Column(String(64))  # 总成绩
    xm = Column(String(64))  # 学生姓名
    xqmc = Column(String(64))  # 学期名称
    kcxzmc = Column(String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(String(64))  # 课程名称
    xf = Column(String(10))  # 学分
    bj = Column(String(64))  # 班级


class yijiu(Base):
    __tablename__ = 'yijiu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(64))  # 学号
    bz = Column(String(64))  # 未知
    cjbsmc = Column(String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(String(64))  # 课程类别名称
    zcj = Column(String(64))  # 总成绩
    xm = Column(String(64))  # 学生姓名
    xqmc = Column(String(64))  # 学期名称
    kcxzmc = Column(String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(String(64))  # 课程名称
    xf = Column(String(10))  # 学分
    bj = Column(String(64))  # 班级


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:03190319@localhost:3306/grade', pool_recycle=3600)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
# if __name__ == '__main__':
#     session = DBSession()
#     user = session.query().all()
