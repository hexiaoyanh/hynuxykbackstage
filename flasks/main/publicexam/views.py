"""
@File : views.py
@Author: Mika
@Date : 2020/4/7
@Desc :
"""
from flask import request, jsonify

from . import publicexam


@publicexam.route('/cetgetverify', methods=['GET', 'POST'])
def cetgetverify():
    data = request.get_json()
    from main.sdk.hynuxykSpider.api.cet import cet
    try:
        cets = cet(data['id_num'], data['name'])
        return jsonify(cets.get_img())
    except Exception:
        return jsonify({"code": "-1", "Msg": "服务器出现错误"})


@publicexam.route('/cetgetscore', methods=['GET', 'POST'])
def cetgetscore():
    data = request.get_json()
    from main.sdk.hynuxykSpider.api.cet import cet
    try:
        cets = cet(data['id_num'], data['name'])
        return jsonify(cets.get_score(data['capcha'], data['cookie']))
    except Exception:
        return jsonify({"code": "-1", "Msg": "服务器出现错误"})

@publicexam.route('/ntcegetverify',methods=['GET','POST'])
def ntcegetverify():
    from main.sdk.hynuxykSpider.api.ntce import ntce
    try:
        ntces = ntce("","")
        return jsonify(ntces.get_img())

    except Exception:
        return jsonify({"code": "-1", "Msg": "服务器出现错误"})