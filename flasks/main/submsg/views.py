"""
@File : views.py
@Author: Mika
@Date : 2019/12/23
@Desc :
"""
import json
import os

from flask import request
import requests
from . import submsg


@submsg.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json()
    parm = {
        "appid": "1110305530",
        "secret": os.environ['qqsecret'],
        "js_code": data['code'],
        "grant_type": "authorization_code"
    }
    data = requests.get(url="https://api.q.qq.com/sns/jscode2session", params=parm)
    print(data.text)
    return data.text


import time


def getaccesstoken():
    with open("access_token.json", "r") as f:
        try:
            data = json.loads(f.read())
            if time.time() - float(data['time']) < 7200:
                print(data['token'])
                return data['token']
        except json.decoder.JSONDecodeError:
            pass
    with open("access_token.json", 'w') as f:
        # 获取accesstoken
        params = {
            "grant_type": "client_credential",
            "appid": "1110305530",
            "secret": os.environ['qqsecret']
        }
        token = requests.get(url="https://api.q.qq.com/api/getToken", params=params)
        token = json.loads(token.text)
        data = {
            "time": str(time.time()),
            "token": token['access_token']
        }
        f.write(json.dumps(data, ensure_ascii=False))
        return data['token']


@submsg.route('/subappmsg', methods=['GET', 'POST'])
def subappmsg():
    data = request.get_json()
    access_token = getaccesstoken()

    return "ok"


@submsg.route('/test')
def test():
    token = getaccesstoken()
    data = {
        "touser": "B89E5A2C3835F554123F50C8D045B26A",
        "template_id": "3e96cab7551f191674a3e75809350f7c",
        "page": "pages/index/",
        "data": {
            "keyword1": {
                "value": "课程名称2"
            },
            "keyword2": {
                "value": "上课时间2"
            },
            "keyword3": {
                "value": "上课地点2"
            },
            "keyword4": {
                "value": "上课人"
            }
        },
        "emphasis_keyword": "keyword1.DATA"
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url="https://api.q.qq.com/api/json/subscribe/SendSubscriptionMessage?access_token=" + token,
                        data=json.dumps(data), headers=headers)
    print(res.text)
    return "ok"
