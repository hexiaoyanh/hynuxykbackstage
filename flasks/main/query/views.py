from flask import request, json, jsonify

from . import query
from ..hynuxykSpider.api import api


@query.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username != None and password != None:
        try:
            logins = api(username, password)
            Msg = logins.getmsg()
            if Msg != "OK":
                return jsonify({"Msg": "Error"})
            jsons = {
                "Msg": "OK",
                "cookie": logins.getcookie()
            }
            return jsonify(jsons)
        except:
            return jsonify({"Msg": "Error"})


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


@query.route('/pscj', methods=['POST'])
def pscj():
    data = request.get_json()
    url = data['url']
    cookie = data['cookie']
    pscj = api(cookie)
    return pscj.querypscj(url)


@query.route('/getMsg', methods=['POST'])
def getMsg():
    import os
    msg = os.environ.get("msg")
    if msg is not None:
        return jsonify({
            "code": 1,
            "msg": msg
        })
    else:
        return jsonify({
            "code": 0
        })


@query.route('/setMsg', methods=['GET', 'POST'])
def setMsg():
    import os
    data = request.get_json()
    psw = os.environ.get("psw")
    if data['psw'] != psw:
        return "您没资格改"
    os.environ["msg"] = data['msg']
    print(os.environ["msg"])
    return "修改成功"
