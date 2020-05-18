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
    #
    # dayi_shang_num = Column(db.String(64))  # 大一上总分
    # dayi_xia_num = Column(db.String(64))  # 大一下总分
    # daer_shang_num = Column(db.String(64))
    # daer_xia_num = Column(db.String(64))
    # dasan_shang_num = Column(db.String(64))
    # dasan_xia_num = Column(db.String(64))
    # dasi_shang_num = Column(db.String(64))
    # dasi_xia_num = Column(db.String(64))
    #
    # dayi_shang_ave = Column(db.String(64))  # 大上一平均分
    # dayi_xia_ave = Column(db.String(64))  # 大一下平均分
    # daer_shang_ave = Column(db.String(64))
    # daer_xia_ave = Column(db.String(64))
    # dasan_shang_ave = Column(db.String(64))
    # dasan_xia_ave = Column(db.String(64))
    # dasi_shang_ave = Column(db.String(64))
    # dasi_xia_ave = Column(db.String(64))
    #
    # dayi_shang_gpa = Column(db.String(64))  # 大一上gpa
    # daer_shang_gpa = Column(db.String(64))
    # dasan_shang_gpa = Column(db.String(64))
    # dasi_shang_gpa = Column(db.String(64))
    # dayi_xia_gpa = Column(db.String(64))
    # daer_xia_gpa = Column(db.String(64))
    # dasan_xia_gpa = Column(db.String(64))
    # dasi_xia_gpa = Column(db.String(64))
    #
    # dayi_shang_xf = Column(db.String(64))  # 大一上学分
    # dayi_xia_xf = Column(db.String(64))
    # daer_shang_xf = Column(db.String(64))
    # daer_xia_xf = Column(db.String(64))
    # dasan_shang_xf = Column(db.String(64))
    # dasan_xia_xf = Column(db.String(64))
    # dasi_shang_xf = Column(db.String(64))
    # dasi_xia_xf = Column(db.String(64))

    # grade = relationship('grade', secondary=user_grade, backref=backref('grade'))
    def __repr__(self):
        return "<User " + self.xh + " " + self.xm + " " + self.yxmc + " " + self.zymc + ">"


# class Grade(db.Model):
#     __tablename__ = 'grade'
#     id = Column(db.Integer, primary_key=True, autoincrement=True)
#     userid = Column(db.String(64))  # 学号
#     bz = Column(db.String(64))  # 未知
#     cjbsmc = Column(db.String(64))  # 特殊情况通报，例如“作弊”“缺考”
#     kclbmc = Column(db.String(64))  # 课程类别名称
#     zcj = Column(db.String(64))  # 总成绩
#     xm = Column(db.String(64))  # 学生姓名
#     xqmc = Column(db.String(64))  # 学期名称
#     kcxzmc = Column(db.String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
#     ksxzmc = Column(
#         db.String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
#     kcmc = Column(db.String(64))  # 课程名称
#     xf = Column(db.String(10))  # 学分
#     bj = Column(db.String(64))

class yiliu(db.Model):
    __tablename__ = 'yiliu'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    userid = Column(db.String(64))  # 学号
    bz = Column(db.String(64))  # 未知
    cjbsmc = Column(db.String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(db.String(64))  # 课程类别名称
    zcj = Column(db.String(64))  # 总成绩
    xm = Column(db.String(64))  # 学生姓名
    xqmc = Column(db.String(64))  # 学期名称
    kcxzmc = Column(db.String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        db.String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(db.String(64))  # 课程名称
    xf = Column(db.String(10))  # 学分
    bj = Column(db.String(64))


class yiqi(db.Model):
    __tablename__ = 'yiqi'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    userid = Column(db.String(64))  # 学号
    bz = Column(db.String(64))  # 未知
    cjbsmc = Column(db.String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(db.String(64))  # 课程类别名称
    zcj = Column(db.String(64))  # 总成绩
    xm = Column(db.String(64))  # 学生姓名
    xqmc = Column(db.String(64))  # 学期名称
    kcxzmc = Column(db.String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        db.String(64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(db.String(64))  # 课程名称
    xf = Column(db.String(10))  # 学分
    bj = Column(db.String(64))


class yiba(db.Model):
    __tablename__ = 'yiba'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    userid = Column(db.String(64))  # 学号
    bz = Column(db.String(64))  # 未知
    cjbsmc = Column(db.String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(db.String(64))  # 课程类别名称
    zcj = Column(db.String(64))  # 总成绩
    xm = Column(db.String(64))  # 学生姓名
    xqmc = Column(db.String(64))  # 学期名称
    kcxzmc = Column(db.String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        db.String(
            64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(db.String(64))  # 课程名称
    xf = Column(db.String(10))  # 学分
    bj = Column(db.String(64))


class yijiu(db.Model):
    __tablename__ = 'yijiu'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    userid = Column(db.String(64))  # 学号
    bz = Column(db.String(64))  # 未知
    cjbsmc = Column(db.String(64))  # 特殊情况通报，例如“作弊”“缺考”
    kclbmc = Column(db.String(64))  # 课程类别名称
    zcj = Column(db.String(64))  # 总成绩
    xm = Column(db.String(64))  # 学生姓名
    xqmc = Column(db.String(64))  # 学期名称
    kcxzmc = Column(db.String(64))  # 课程性质名称，根据此项不同值可判断该科成绩是否计入GPA
    ksxzmc = Column(
        db.String(
            64))  # 考试性质名称, 目前遇见的情况有正常考试，补考（x），重修（x），分别意为补考第x次和重修第x次，若补考未通过，正常考试条目和补考条目将同时存在，若补考通过，则只存在补考条目
    kcmc = Column(db.String(64))  # 课程名称
    xf = Column(db.String(10))  # 学分
    bj = Column(db.String(64))

    def __repr__(self):
        return "<Grade " + self.userid + " " + self.xm + " " + self.xqmc + " " + self.zcj + ">"
