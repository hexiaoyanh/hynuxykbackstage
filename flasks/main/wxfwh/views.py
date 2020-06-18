import hashlib
import json
import time

import requests
import xmltodict as xmltodict
from flask import request, make_response, jsonify
from flask_login import login_user, login_required, current_user
from . import wxfwh
from main import db
from .. import access_token
from ..models import WXUser


def dealtextmsg(fromusername, tousername):
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": u"我只是一只小白兔，还在进化当中^_^",
    }


def dealsubscrible(fromusername, tousername):
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": u"欢迎关注衡师小助手的微信服务号，功能还在开发当中呢。",
    }


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
            msgtype = resp_dict.get('MsgType')
            fromusername = resp_dict.get('FromUserName')
            tousername = resp_dict.get('ToUserName')
            if 'text' == msgtype:
                response = dealtextmsg(fromusername, tousername)
            elif msgtype == 'event':
                event = resp_dict.get('Event')
                if event == 'subscribe':
                    response = dealsubscrible(fromusername, tousername)
                else:
                    response = {
                        "ToUserName": resp_dict.get('FromUserName'),
                        "FromUserName": resp_dict.get('ToUserName'),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": u"暂不支持的消息",
                    }
            else:
                response = {
                    "ToUserName": resp_dict.get('FromUserName'),
                    "FromUserName": resp_dict.get('ToUserName'),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": u"暂不支持的消息",
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


@wxfwh.route('/islogin')
def islogin():
    if current_user.is_authenticated:
        return jsonify({'code': 1})
    else:
        return jsonify({'code': -1})
