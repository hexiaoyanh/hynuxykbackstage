from flask import request, json, jsonify

from . import query
from ..hynuxykSpider.api import api


@query.route('/kb', methods=['POST'])
def kb():
    # 解析传来的数据
    data = request.get_json()
    date = data['date']
    week = data['week']
    if date is None:
        return "You must input date!"
    try:
        # 如果是cookie
        cookies = data['cookies']
        kb = api(cookies)
    except:
        try:
            username = data['username']
            password = data['password']
            kb = api(username, password)
        except:
            return "error"
    jsons = {
        "kb": kb.querykb(date, week),
        'cookie': kb.getcookie()
    }
    return jsonify(jsons)


@query.route('/cj', methods=['POST'])
def cj():
    data = request.get_json()
    date = data['date']
    week = data['week']
    if date is None:
        return "You must input date!"
    try:
        # 如果是cookie
        cookies = data['cookies']
        cj = api(cookies)
    except:
        try:
            username = data['username']
            password = data['password']
            cj = api(username, password)
        except:
            return "error"
    jsons = {
        'cj': cj.querycj(date),
        'cookie': cj.getcookie()
    }
    return jsonify(jsons)
