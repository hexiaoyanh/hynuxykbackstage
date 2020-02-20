from flask import request, json, jsonify

from . import query


@query.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    nanyue = None
    if data.get("nanyue") is None:
        nanyue = False
    else:
        nanyue = data['nanyue']
    if username != None and password != None:
        try:
            from ..hynuxykSpider.api.jwlogin import jwlogin
            logins = jwlogin(username, password, nanyue)
            Msg = logins.Msg
            if Msg != "OK":
                return jsonify({"Msg": Msg})
            jsons = {
                "Msg": "OK",
                "cookie": logins.cookie
            }
            return jsonify(jsons)
        except EOFError:
            return jsonify({"Msg": "服务器错误"})


@query.route('/kb', methods=['POST'])
def kb():
    # 解析传来的数据
    data = request.get_json()
    date = data['date']
    week = data['week']
    if data.get("nanyue") is None:
        nanyue = False
    else:
        nanyue = data['nanyue']
    if date is None:
        return "You must input date!"
        # 如果是cookie
    cookies = data['cookies']

    from main.hynuxykSpider.api.querykb import querykb
    kb = querykb(cookies, nanyue)

    jsons = {
        "kb": kb.queryallkb(date, week),
        'cookie': kb.cookie
    }
    return jsonify(jsons)


@query.route('/cj', methods=['POST'])
def cj():
    data = request.get_json()
    date = data['date']
    if date is None:
        return "You must input date!"

    cookies = data['cookies']
    if data.get("nanyue") is None:
        nanyue = False
    else:
        nanyue = data['nanyue']

    from main.hynuxykSpider.api.querycj import querycj
    cj = querycj(cookies, nanyue)

    jsons = {
        'cj': json.dumps(cj.queryallcj(date), ensure_ascii=False),
        'cookie': cj.cookie
    }
    return jsonify(jsons)


@query.route('/pscj', methods=['POST'])
def pscj():
    data = request.get_json()
    url = data['url']
    cookie = data['cookie']
    if data.get("nanyue") is None:
        nanyue = False
    else:
        nanyue = data['nanyue']
    from ..hynuxykSpider.api.queryqxcj import querypscj
    pscj = querypscj(url, cookie, nanyue)
    return pscj


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
