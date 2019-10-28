from flask import request, json, jsonify

from . import query
from ..hynuxykSpider.api import api


@query.route('/kb', methods=['POST'])
def kb():
    username = request.form.get('username')
    password = request.form.get('password')
    date = request.form.get('date')
    cookies = request.form.get('cookies')
    week = request.form.get('week')
    if date is None:
        return "You must input date!"
    if (username is None and password is None) and cookies is None:
        return "You must input username and password or input cookies"
    if cookies is None:
        kb = api(username, password)
    else:
        kb = api(cookies)
    jsons = {
        "kb": kb.querykb(date, week),
        'cookie': kb.getcookie()
    }
    return jsonify(jsons)


@query.route('/cj', methods=['POST'])
def cj():
    username = request.form.get('username')
    password = request.form.get('password')
    date = request.form.get('date')
    cookies = request.form.get('cookies')
    if date is None:
        return "You must input date!"
    if (username is None and password is None) and cookies is None:
        return "You must input username and password or input cookies"
    if cookies is None:
        cj = api(username, password)
    else:
        cj = api(cookies)
    jsons = {
        'cj': cj.querycj(date),
        'cookie': cj.getcookie()
    }
    return jsonify(jsons)
