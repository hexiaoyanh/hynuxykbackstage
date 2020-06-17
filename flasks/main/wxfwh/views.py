import hashlib
import json
import os
import time

import requests
import xmltodict as xmltodict
from flask import request, make_response, jsonify
from flask_login import login_user, current_user, login_required

from . import wxfwh
from .get_access_token import get_access_token
from .. import db
from ..models import WXUser

access_token = get_access_token()


# 微信服务号的token验证
@wxfwh.route('/wx', methods=['GET', 'POST'])
def getinput():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = "mikahemikahe"
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    sha1.update(list[0].encode('utf-8'))
    sha1.update(list[1].encode('utf-8'))
    sha1.update(list[2].encode('utf-8'))
    hashcode = sha1.hexdigest()

    if hashcode == signature:
        if request.method == 'GET':
            return echostr
        else:
            resp_data = request.data
            resp_dict = xmltodict.parse(resp_data).get('xml')
            print(resp_dict)
            # 如果是文本消息
            if 'text' == resp_dict.get('MsgType'):
                response = {
                    "ToUserName": resp_dict.get('FromUserName'),
                    "FromUserName": resp_dict.get('ToUserName'),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": resp_dict.get('Content'),
                }
            else:
                response = {
                    "ToUserName": resp_dict.get('FromUserName'),
                    "FromUserName": resp_dict.get('ToUserName'),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": u"暂时只支持文字呢",
                }
            if response:
                response = {"xml": response}
                response = xmltodict.unparse(response)
            else:
                response = ''
            return make_response(response)
    else:
        return ""


# 获取用户信息
def getopenidmsg(user, openid, access_token):
    res = requests.get(
        url="https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN")
    res = json.loads(str(res.content, 'utf-8'))
    user.nicename = res['nickname']
    user.sex = int(res['sex'])
    user.province = res['province']
    user.city = res['city']
    user.country = res['country']
    user.headimgurl = res['headimgurl']
    return user


@wxfwh.route('/login/<string:code>', methods=['GET'])
def login(code):
    res = access_token.code2access_token(code)
    if res.get('errcode') is not None:
        return jsonify({
            "code": "-1",
            "msg": res['errmsg']
        })
    user = WXUser.query.filter(WXUser.openid == res['openid']).first()
    if user is None:
        user = WXUser(openid=res['openid'], access_token=res['access_token'], refresh_token=res['refresh_token'])
        user = getopenidmsg(user, res['openid'], res['access_token'])
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return jsonify({
        "code": 1,
        "msg": "登录成功"
    })



# @wxfwh.route('/test')
# def test():
#     data = {
#         "touser": "oOMYrw9BmYjBr882e9XAmG61uozY",
#         "template_id": "xuySp_1jAdlVUqh2flrO8TtbCx3_FZA8dBLBhC-VAuM",
#         "url": "",
#         "data": {
#             "first": {
#                 "value": "您有一节课将在30分钟后开始！",
#                 "color": "#173177"
#             },
#             "keyword1": {
#                 "value": "英语",
#                 "color": "#173177"
#             },
#             "keyword2": {
#                 "value": "8:30",
#                 "color": "#173177"
#             },
#             "keyword3": {
#                 "value": "Mika",
#                 "color": "#173177"
#             },
#             "keyword4": {
#                 "value": "8:30",
#                 "color": "#173177"
#             },
#             "keyword5": {
#                 "value": "10:30",
#                 "color": "#173177"
#             },
#             "keyword6": {
#                 "value": "计科楼511",
#                 "color": "#173177"
#             }
#         }
#     }
#     print(data)
#     access_tokens = access_token.get_access_token()
#     headers = {
#         "Content-Type": "application/json"
#     }
#     print(access_tokens)
#     res = requests.post(url=" https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_tokens,
#                         data=json.dumps(data), headers=headers)
#     print(res.text)
#     return "ok"
