import hashlib
import json
import time

import requests
import xmltodict as xmltodict
from flask import request, make_response, jsonify
from flask_login import login_user, login_required, current_user
from . import wxfwh
from main import db, nowdates
from .sendnotification import send_exam_notification
from .. import access_token
from ..models import WXUser
from ..verifyjw import verifyjw


def dealtextmsg(content, fromusername, tousername):
    msg = u"我收到啦，看到信息就回你"
    if '成绩' in content:
        wxuser = WXUser.query.filter(WXUser.openid == fromusername).first()
        if wxuser is None or wxuser.userid is None:
            msg = u"这里没有你的教务网账号哦，请前往[订阅通知]-[绑定教务网]绑定你的教务网账号哦(*^▽^*)"
        else:
            token = verifyjw.login(wxuser.userid, wxuser.password)
            exam = verifyjw.get_exam(token, wxuser.userid, nowdates.get()['xn'])
            # exam = verifyjw.get_exam(token, wxuser.userid, "2019-2020-1")
            if len(exam) == 1 and exam[0] is None:
                msg = u"你这个学期都还没有成绩粗来(〃＞皿＜)"
            else:
                msg = ""
                for i in exam:
                    msg += "考试名称：" + i['kcmc'] + '\n' + "考试性质：" + i['ksxzmc'] + '\n' + "课程性质：" + i[
                        'kclbmc'] + '\n' + "总成绩：" + i['zcj'] + '\n\n'
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": msg+"或者前往小程序-【课表成绩】-【成绩】查询当前学期的成绩或排名",
    }


def dealsubscrible(fromusername, tousername):
    send_exam_notification(fromusername, "美丽程度", "100昏！")
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": u"欢迎关注衡师小助手的微信服务号，绑定教务网可以推送成绩信息给你，所有的功能都能使用，遇到什么问题发信息给我啦QAQ",
    }


def sub_exam_notificate(fromusername, tousername):
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": u"订阅考试通知需要绑定教务账号哦，请前往[订阅通知]-[绑定教务网]绑定你的教务网账号，绑定成功会自动订阅啦。",
    }


def dealunsubscrible(fromusername, tousername):
    user = WXUser.query.filter(WXUser.openid == fromusername).first()
    if user is None:
        return ""
    db.session.delete(user)
    db.session.commit()
    return ""


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
            response = None
            if 'text' == msgtype:
                content = resp_dict.get('Content')
                response = dealtextmsg(content, fromusername, tousername)
            elif msgtype == 'event':
                event = resp_dict.get('Event')
                if event == 'subscribe':
                    response = dealsubscrible(fromusername, tousername)
                elif event == 'unsubscribe':
                    response = dealunsubscrible(fromusername, tousername)
                elif event == 'CLICK':
                    eventclick = resp_dict.get('EventKey')
                    if eventclick == 'sub_exam_notification':
                        response = sub_exam_notificate(fromusername, tousername)
            if response is not None:
                response = {"xml": response}
                response = xmltodict.unparse(response)
            else:
                response = {
                    "ToUserName": resp_dict.get('FromUserName'),
                    "FromUserName": resp_dict.get('ToUserName'),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": u"暂不支持的消息",
                }
            return make_response(response)
    else:
        return ""


# 获取用户信息
def get_open_id_msg(user, openid, access_token):
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
        user = get_open_id_msg(user, res['openid'], res['access_token'])
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
