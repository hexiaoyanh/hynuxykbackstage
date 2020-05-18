from . import rank
from flask import request, jsonify
from ..models import User, yiliu, yiqi, yiba, yijiu


rank2grade = {
    "优": 95,
    "良": 85,
    "中": 75,
    "及格": 60,
    "合格":60,
    "不及格": 0,
    "通过": 60
}

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def getgrade(xh, xqmc):
    if xh[:2] == "16":
        return yiliu.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "17":
        return yiqi.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "18":
        return yiba.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "19":
        return yijiu.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()


def gettotalrank(js, xh):
    js = sorted(js, key=lambda x: (print(x), float(x['allnum'])), reverse=True)
    print(js)

    flag = 1
    for i in js:
        if i['xh'] == xh: return flag
        flag += 1


@rank.route('/getclassallrank')
def getclassrank():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(xh=data['userid']).first()
    useres = User.query.filter(User.bj == user.bj).all()
    people = []
    classlen = len(useres)
    res = []
    for i in useres:
        grade = getgrade(i.xh, data['xqmc'])
        classlen = len(grade)
        if classlen == 0:
            msg = {
                "xh": i.xh,
                "averagescore": 0,
                "allnum": 0,
                "allgpa": 0,
                "gpa": 0,
                "xf": 0
            }
            people.append(msg)
            continue
        xf = 0
        allnum = 0
        gpa = 0
        for j in grade:
            xf += float(j.xf)
            if is_contains_chinese(j.zcj):
                allnum += rank2grade[j.zcj]
                if (rank2grade[j.zcj] >= 60): gpa += 4 - 3 * (100 - rank2grade[j.zcj]) ** 2 / 1600
            else:
                allnum += float(j.zcj)
                num = float(j.zcj)
                if num >= 60: gpa += 4 - 3 * (100 - num) ** 2 / 1600
        msg = {
            "xh": i.xh,
            "km": classlen,
            "averagescore": format(allnum / classlen, '.2f'),
            "allnum": format(allnum, '.2f'),
            "allgpa": format(gpa, '.2f'),
            "gpa": format(gpa / xf, '.2f'),
            "xf": xf
        }
        people.append(msg)
    classrank = gettotalrank(people, data['userid'])
    print(classrank)
    return jsonify(people)
