from . import rank
from flask import request, jsonify
from ..models import User, yiliu, yiqi, yiba, yijiu
from .sqlfunc import select_data

rank2grade = {
    "优": 95,
    "良": 85,
    "中": 75,
    "及格": 60,
    "合格": 60,
    "不及格": 0,
    "通过": 60
}

import time, math


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


@rank.route('/getrankmsg',methods=['GET','POST'])
def getrankmsg():
    data = request.get_json()
    user = User.query.get(data['userid'])
    useres = User.query.filter_by(bj=user.bj).all()
    people = []
    for i in useres:
        grade = select_data(i.xh[:4], i.xh, data['xqmc'])
        total_num = 0  # 总分
        total_credit = 0  # 总学分
        total_pku_gpa = 0  # 北大gpa
        total_ave_gpa = 0  # 平均学分绩点
        for j in grade:
            global num
            if is_contains_chinese(j[5]):
                num = rank2grade[j[5]]
                total_num += num
                if num >= 60:
                    total_pku_gpa += 4 - 3 * (100 - num) ** 2 / 1600 * float(j[11])
            else:
                num = float(j[5])
                total_num += num
                if num >= 60:
                    total_pku_gpa += (4 - 3 * (100 - num) ** 2 / 1600) * float(j[11])
            # print(j[6], j[11], float(j[11]))
            total_credit += float(j[11])
            total_ave_gpa += num * float(j[11])
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
    classrank = 1
    for i in people:
        if i['xh'] == data['userid']: break
        classrank += 1
    userdata = people[classrank - 1]  # 获取需要查询的用户数据
    userdata['num_rank'] = numrank  # 添加总分排名
    userdata['pku_gpa_rank'] = pkurank
    userdata['avegpa_rank'] = avegpa_rank
    return jsonify(userdata)
