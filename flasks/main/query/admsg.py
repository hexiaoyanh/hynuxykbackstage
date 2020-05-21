"""
@File : admsg.py
@Author: Mika
@Date : 2020/4/20
@Desc :
"""
import datetime
import json

from flask import request

from . import query
import requests


@query.route('/viewadd', methods=['GET', 'POST'])
def viewadd():
    data = request.get_json()
    requests.get("https://sc.ftqq.com/SCU77855T4c90b9b4eca19f5ca3e3f47d8277a33e5e201bee5d183.send?text="+ data['username']+"看广告了")
    nowtime = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(
        datetime.datetime.now().day) + ".json"
    try:
        with open(nowtime, 'r', encoding='utf-8') as f:
            res = json.loads(f.read(), encoding='utf-8')
        with open(nowtime, 'w', encoding='utf-8') as f:
            try:
                res[data['userid']]['adviewnum'] += 1
                f.truncate()
                f.write(json.dumps(res, ensure_ascii=False))
            except KeyError:
                sss = {
                    "username": data['username'],
                    "adviewnum": 1
                }
                res[data['userid']] = sss
                f.write(json.dumps(res, ensure_ascii=False))
        return "ok"
    except FileNotFoundError:
        with open(nowtime, 'w', encoding='utf-8') as f:
            res = {}
            sss = {
                "username": data['username'],
                "adviewnum": 1
            }
            res[data['userid']] = sss
            f.write(json.dumps(res, ensure_ascii=False))
        return "ok"


@query.route('/getviewad', methods=['GET'])
def getviewad():
    nowtime = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(
        datetime.datetime.now().day) + ".json"
    try:
        with open(nowtime, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return json.dumps("",ensure_ascii=False)