from flask_login import login_required

from . import rank
from flask import request, jsonify, abort
from ..models import User, Usern, Grade
from .. import db
from ..verifyjw import verifyjw
from ..wxfwh.sendnotification import send_ad_notification, send_update_notifications

rank2grade = {
    "优": 95,
    "良": 85,
    "中": 75,
    "及格": 60,
    "合格": 60,
    "不及格": 0,
    "通过": 60
}


# 判断是否含中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# 获取排名
def getrank(people, userid, obj):
    people = sorted(people, key=lambda x: float(x[obj]), reverse=True)
    rank = 1
    for i in people:
        if i['xh'] == userid: break
        rank += 1
    return rank


def is_illegal(userid):
    for i in userid:
        if i not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'N']:
            return True
    return False


@rank.route('/getrankmsg', methods=['GET', 'POST'])
def getrankmsg():
    data = request.get_json()
    if data.get('elective') is not None:
        elective = data['elective']
    else:
        elective = False
    # 防止sql注入
    if is_illegal(data['userid']): abort(500)
    if data['userid'][0] == 'N':
        user = Usern.query.get(data['userid'])
        useres = Usern.query.filter_by(bj=user.bj).all()
    else:
        user = User.query.get(data['userid'])
        useres = User.query.filter_by(bj=user.bj).all()
    people = []
    for i in useres:
        # grade = select_data(db, i.xh[:5], i.xh, data['xqmc'], elective)
        if elective:
            grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == data['xqmc']).all()
        else:
            grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == data['xqmc'], Grade.kclbmc != '公选').all()

        total_num = 0  # 总分
        total_credit = 0  # 总学分
        total_pku_gpa = 0  # 北大gpa
        total_ave_gpa = 0  # 平均学分绩点
        for j in grade:
            global num
            if is_contains_chinese(j.zcj):
                num = rank2grade[j.zcj]
                total_num += num
                if num >= 60:
                    total_pku_gpa += (4 - 3 * (100 - num) ** 2 / 1600.0) * float(j.xf)
            else:
                num = float(j.zcj)
                total_num += num
                if num >= 60:
                    total_pku_gpa += (4 - 3 * (100 - num) ** 2 / 1600.0) * float(j.xf)
            # print(j[6], j[11], float(j[11]))
            total_credit += float(j.xf)
            total_ave_gpa += num * float(j.xf)
        # 北京大学gpa计算
        total_pku_gpa = total_pku_gpa / total_credit if total_credit != 0 else 0
        total_ave_gpa = total_ave_gpa / total_credit if total_credit != 0 else 0
        userdata = {
            "xh": i.xh,
            "xm": i.xm,
            "total_num": round(total_num, 2),
            "total_pku_gpa": round(total_pku_gpa, 2),
            "total_credit": round(total_credit, 2),
            "total_ave_gpa": round(total_ave_gpa, 2),
            "average_num": round(total_num / len(grade) if len(grade) != 0 else 0, 2)
        }
        people.append(userdata)

    # 获取总分排名
    numrank = getrank(people, data['userid'], "total_num")
    pkurank = getrank(people, data['userid'], 'total_pku_gpa')
    avegpa_rank = getrank(people, data['userid'], 'total_ave_gpa')
    average_num_rank = getrank(people, data['userid'], 'average_num')
    classrank = 1
    for i in people:
        if i['xh'] == data['userid']: break
        classrank += 1
    userdata = people[classrank - 1]  # 获取需要查询的用户数据
    userdata['num_rank'] = numrank  # 添加总分排名
    userdata['pku_gpa_rank'] = pkurank
    userdata['avegpa_rank'] = avegpa_rank
    userdata['average_num_rank'] = average_num_rank
    return jsonify(userdata)


@rank.route('/findyou', methods=['GET', 'POST'])
def findyou():
    data = request.get_json()
    if data['userid'] != "":
        if data['userid'][0] == 'N':
            useres = Usern.query.get(data['userid'])
        else:
            useres = User.query.get(data['userid'])
        if useres is None:
            return jsonify({
                "code": -1,
                "msg": "没有找到这个人哦。"
            })
        js = {}
        js['code'] = 1
        js['msg'] = "查询成功"
        js[useres.xh] = {
            "xh": useres.xh,
            "xm": useres.xm,
            "bj": useres.bj,
            "xymc": useres.yxmc,
            "nj": useres.nj
        }
        return jsonify(js)
    elif data['xm'] != "":
        useres1 = User.query.filter_by(xm=data['xm']).all()
        useres2 = Usern.query.filter_by(xm=data['xm']).all()
        if len(useres1) == 0 and len(useres2) == 0:
            return jsonify({
                "code": -1,
                "msg": "没有找到这个人哦。"
            })
        js = {}
        js['code'] = 1
        js['msg'] = "查询成功"
        for i in useres1:
            js[i.xh] = {
                "xh": i.xh,
                "xm": i.xm,
                "bj": i.bj,
                "xymc": i.yxmc,
                "nj": i.nj
            }
        for i in useres2:
            js[i.xh] = {
                "xh": i.xh,
                "xm": i.xm,
                "bj": i.bj,
                "xymc": i.yxmc,
                "nj": i.nj
            }
        return jsonify(js)


@rank.route('/update_class_info')
def update_class_info():
    class_name = request.args.get('class_name')
    for i in range(1, 100):
        userid = class_name
        if i <= 9:
            userid += "0" + str(i)
        else:
            userid += str(i)
        if userid[0] == 'N':
            user = Usern.query.filter(Usern.xh == userid).first()
        else:
            user = User.query.filter(User.xh == userid).first()
        if user is not None: continue
        if user is None:
            from ..verifyjw import verifyjw
            info = verifyjw.get_user_info(userid)
            print(userid)
            print(info)
            if info == {}: continue
            if userid[0] == 'N':
                user = Usern(fxzy=info['fxzy'], xh=info['xh'], xm=info['xm'], dqszj=info['dqszj'], yxmc=info['yxmc'],
                             xz=info['xz'], bj=info['bj'],
                             dh=info['dh'], email=info['email'], rxnf=info['rxnf'], xb=info['xb'], ksh=info['ksh'],
                             nj=info['nj'], qq=info['qq'], zymc=info['zymc'])
            else:
                user = User(fxzy=info['fxzy'], xh=info['xh'], xm=info['xm'], dqszj=info['dqszj'], yxmc=info['yxmc'],
                            xz=info['xz'], bj=info['bj'],
                            dh=info['dh'], email=info['email'], rxnf=info['rxnf'], xb=info['xb'], ksh=info['ksh'],
                            nj=info['nj'], qq=info['qq'], zymc=info['zymc'])
            db.session.add(user)
            db.session.commit()
        return "ok"


@rank.route('/request_update_exam')
def request_update_exam():
    userid = request.args.get('class_name')
    if userid[0] == 'N':
        user = Usern.query.filter(Usern.xh == userid).first()
    else:
        user = User.query.filter(User.xh == userid).first()
    if user is None:
        return jsonify({
            "code": 1,
            "msg": "学号错误，请输入正确的学号"
        })
    if userid[0] is 'N':
        users = Usern.query.filter(Usern.bj == user.bj).all()
    else:
        users = User.query.filter(Usern.bj == user.bj).all()

    for i in users:
        if i.xh is None or i.xh == "":
            continue
        exam = verifyjw.get_exam("token", i.xh, "2019-2020-2")
        for j in exam:
            if j is None: continue
            grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == "2019-2020-2",
                                       Grade.ksxzmc == j['ksxzmc'], Grade.kcmc == j['kcmc']).first()
            if grade is None:
                grade = Grade(userid=i.xh, bz=j['bz'], cjbsmc=j['cjbsmc'], kclbmc=j['kclbmc'], zcj=j['zcj'],
                              xm=i.xm, xqmc=j['xqmc'], kcxzmc=j['kcxzmc'], ksxzmc=j['ksxzmc'], kcmc=j['kcmc'],
                              xf=j['xf'], bj=i.bj)
                db.session.add(grade)
                db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "更新完成"
    })


@rank.route('/update_class_exams')
def update_class_exam():
    class_name = request.args.get('class_name')[:-2]
    # send_ad_notification("更新" + class_name, xn)
    if class_name[0] is 'N':
        users = Usern.query.filter(Usern.xh.like(class_name + '%')).all()
    else:
        users = User.query.filter(User.xh.like(class_name + '%')).all()
    for i in users:
        if i.xh is None or i.xh == "":
            continue
        exam = verifyjw.get_exam("token", i.xh, "2019-2020-2")
        for j in exam:
            if j is None: continue
            grade = Grade.query.filter(Grade.userid == i.xh, Grade.xqmc == "2019-2020-2",
                                       Grade.ksxzmc == j['ksxzmc'], Grade.kcmc == j['kcmc']).first()
            if grade is None:
                grade = Grade(userid=i.xh, bz=j['bz'], cjbsmc=j['cjbsmc'], kclbmc=j['kclbmc'], zcj=j['zcj'],
                              xm=i.xm, xqmc=j['xqmc'], kcxzmc=j['kcxzmc'], ksxzmc=j['ksxzmc'], kcmc=j['kcmc'],
                              xf=j['xf'], bj=i.bj)
                db.session.add(grade)
                db.session.commit()
    return "已更新学号前6位为" + class_name + "的所有人"
