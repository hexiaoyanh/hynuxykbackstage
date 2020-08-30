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
from ..models import WXUser, Keywords
from ..verifyjw import verifyjw


def generate_return(msg, fromusername, tousername):
    return {
        "ToUserName": fromusername,
        "FromUserName": tousername,
        "CreateTime": int(time.time()),
        "MsgType": "text",
        "Content": msg
    }


def dealtextmsg(content, fromusername, tousername):
    if '成绩' in content:
        wxuser = WXUser.query.filter(WXUser.openid == fromusername).first()
        if wxuser is None or wxuser.userid is None:
            keyword = Keywords.query.filter(Keywords.keyword == 'can_not_find_account').first()
            return generate_return(keyword.reply, fromusername, tousername)
        else:
            try:
                exam = verifyjw.get_exam("token", wxuser.userid, nowdates.get()['xn'])
            # 教务网不可访问的错误s
            except requests.exceptions.ConnectionError:
                keyword = Keywords.query.filter(Keywords.keyword == 'can_not_request_jiaowu').first()
                return generate_return(keyword.reply, fromusername, tousername)
            # exam = verifyjw.get_exam(token, wxuser.userid, "2019-2020-1")
            if len(exam) == 1 and exam[0] is None:
                msg = Keywords.query.filter(Keywords.keyword == 'can_not_request_jiaowu').first().reply
            else:
                msg = ""
                for i in exam:
                    msg += "考试名称：" + i['kcmc'] + '\n' + "考试性质：" + i['ksxzmc'] + '\n' + "课程性质：" + str(i.get('kclbmc')) + '\n' + "总成绩：" + str(i.get('zcj')) + '\n\n'

        return generate_return(msg, fromusername, tousername)
    elif '情话' in content:
        res = requests.get("https://chp.shadiao.app/api.php")
        return generate_return(res.text, fromusername, tousername)
    elif '朋友圈文案' in content:
        res = requests.get("https://pyq.shadiao.app/api.php")
        return generate_return(res.text, fromusername, tousername)
    elif '毒鸡汤' in content:
        res = requests.get("https://du.shadiao.app/api.php")
        return generate_return(res.text, fromusername, tousername)
    else:
        keywords = Keywords.query.all()
        for i in keywords:
            if i.keyword in content:
                return generate_return(i.reply, fromusername, tousername)
        return ""


def dealsubscrible(fromusername, tousername):
    send_exam_notification(fromusername, "美丽程度", "100昏！")
    return generate_return(Keywords.query.filter(Keywords.keyword == 'subscribe').first().reply, fromusername,
                           tousername)


def sub_exam_notificate(fromusername, tousername):
    user = WXUser.query.filter(WXUser.openid == fromusername).first()
    if user is None or user.userid is None:
        return generate_return(Keywords.query.filter(Keywords.keyword == 'can_not_find_account').first(), fromusername,
                               tousername)
    else:
        return generate_return(Keywords.query.filter(Keywords.keyword == 'is_bind_ok').first().reply, fromusername,
                               tousername)


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
            # 如果是文本消息
            print(resp_dict)
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
                    elif eventclick == 'get_exam_score':
                        response = dealtextmsg("成绩", fromusername, tousername)
            if response == "":
                pass
            elif response is not None:
                response = {"xml": response}
                response = xmltodict.unparse(response)
            else:
                response = ""
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
