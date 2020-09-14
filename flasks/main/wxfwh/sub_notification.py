import datetime
import threading
import time

import requests
import xmltodict
from flask import jsonify, request

from . import wxfwh
from flask_login import login_required, current_user

from .pay_settings import random_str, APP_ID, MCH_ID, CREATE_IP, NOTIFY_URL, API_KEY, get_sign, trans_dict_to_xml, \
    trans_xml_to_dict
from .sendnotification import send_success_sub
from main.verifyjw import verifyjw
from .. import db, nowdates, wechatsettings
from ..models import WXUser, Curriculum, Bill


@wxfwh.route('/createsubpay')
@login_required
def createsubpay():
    nonce_str = random_str()  # 拼接出随机的字符串即可，我这里是用 时间+随机数字+5个随机字母
    total_fee = wechatsettings.get_total_fee()  # 付款金额，单位是分，必须是整数
    params = {
        'appid': APP_ID,  # APPID
        'mch_id': MCH_ID,  # 商户号
        'nonce_str': nonce_str,  # 随机字符串
        'out_trade_no': random_str(),  # 订单编号，可自定义
        'total_fee': total_fee,  # 订单总金额
        'spbill_create_ip': CREATE_IP,  # 自己服务器的IP地址
        'notify_url': NOTIFY_URL,  # 回调地址，微信支付成功后会回调这个url，告知商户支付结果
        'body': '衡师小助手',  # 商品描述
        'detail': '订阅上课通知',  # 商品描述
        'trade_type': 'JSAPI',  # jsapi支付类型
        'openid': current_user.openid
    }
    sign = get_sign(params, API_KEY)  # 获取签名
    params['sign'] = sign  # 添加签名到参数字典
    xml = trans_dict_to_xml(params)  # 转换字典为XML
    response = requests.post(url="https://api.mch.weixin.qq.com/pay/unifiedorder", data=xml.encode("utf-8"))
    data_dict = trans_xml_to_dict(response.content)['xml']  # 将请求返回的数据转为字典
    params = {}
    params['appId'] = APP_ID
    params['timeStamp'] = int(time.time())
    params['nonceStr'] = random_str(16)
    params['package'] = 'prepay_id=' + data_dict['prepay_id']
    params['signType'] = 'MD5'
    params['paySign'] = get_sign({'appId': APP_ID,
                                  "timeStamp": params['timeStamp'],
                                  'nonceStr': params['nonceStr'],
                                  'package': 'prepay_id=' + data_dict['prepay_id'],
                                  'signType': 'MD5',
                                  },
                                 API_KEY)

    return jsonify(params)


@wxfwh.route('/get_total_fee')
@login_required
def get_total_fee():
    return jsonify({
        "code": 1,
        "total_fee": wechatsettings.get_total_fee()
    })


@wxfwh.route('/successpay', methods=['GET', 'POST'])
def successpay():
    print(request.data)
    data = xmltodict.parse(request.data)['xml']
    print(data)
    if data['result_code'] == 'SUCCESS':
        send_success_sub(data['openid'], data['transaction_id'], data['total_fee'], data['time_end'])
        user = WXUser.query.filter_by(openid=data['openid']).first()
        bill = Bill(transaction_id=data['transaction_id'], out_trade_no=data['out_trade_no'],
                    total_fee=data['total_fee'], result_code=data['result_code'],
                    openid=data['openid'], create_time=datetime.datetime.now())
        db.session.add(bill)
        nowtime = datetime.datetime.now()
        if nowtime.month < 7:
            nowtime = datetime.datetime(nowtime.year, nowtime.month + 6, nowtime.day)
        else:
            nowtime = datetime.datetime(nowtime.year + 1, nowtime.month + 6 - 12, nowtime.day)

        if not user.is_subnotice:
            GetClass(user.userid, user.password)

        user.server_expire = nowtime
        user.is_subnotice = True
        user.notification_status = True
        user.is_experience = False
        db.session.add(user)
        db.session.commit()
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"


def GetClass(userid, password):
    thr = threading.Thread(target=getclass, args=[userid, password, ])  # 创建线程
    thr.start()


# 同步学校的作息时间
def convert_begintime(s):
    t = s.split(":")
    m = int(t[1])
    h = int(t[0])
    m += 30
    if m >= 60:
        m -= 60
        h += 1
    m = str(m)
    h = str(h)
    if len(h) == 1: h = "0" + h
    if len(m) == 1: m = "0" + m
    return h + ":" + m


def getclass(userid, password):
    # 使用nowdates的app上下文防止导入两次manager导致定时任务重复运行
    with nowdates.app.app_context():
        try:
            token = verifyjw.login(userid, password)
            nowtime = nowdates.get()
            for i in range(25):
                kecheng = verifyjw.getclass(token, userid, nowtime['xn'], str(i))
                for j in kecheng:
                    if j is None: continue
                    curriculum = Curriculum.query.filter_by(userid=userid, school_year=nowtime['xn'], week=i,
                                                            class_time=j['kcsj'],
                                                            class_name=j['kcmc'], teacher=j['jsxm'],
                                                            location=j['jsmc'],
                                                            begintime=convert_begintime(j['kssj']), endtime=j['jssj'],
                                                            cycle=j['kkzc']).first()
                    if curriculum is not None: continue
                    curriculum = Curriculum(userid=userid, school_year=nowtime['xn'], week=i, class_time=j['kcsj'],
                                            class_name=j['kcmc'], teacher=j['jsxm'], location=j['jsmc'],
                                            begintime=j['kssj'], endtime=j['jssj'], cycle=j['kkzc'])
                    db.session.add(curriculum)
            db.session.commit()
        except Exception as e:
            print("错误:", e)


@wxfwh.route('/is_sub_class')
@login_required
def is_sub():
    if current_user.server_expire >= datetime.datetime.now():
        return jsonify({
            "code": 1,
            "msg": "您已订阅上课通知",
            "server_expire": str(current_user.server_expire)
        })
    else:
        return jsonify({
            "code": -1,
            "msg": "您未订阅上课通知"
        })


@wxfwh.route('/close_class_notification')
@login_required
def close_class_notification():
    current_user.notification_status = False
    db.session.add(current_user)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "您已关闭上课通知"
    })


@wxfwh.route('/open_class_notification')
@login_required
def open_class_notification():
    current_user.notification_status = True
    db.session.add(current_user)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "您已开启上课通知"
    })


@wxfwh.route('/get_notification_status')
@login_required
def get_notification_status():
    if current_user.notification_status:
        return jsonify({
            "code": 1
        })
    else:
        return jsonify({
            "code": -1
        })
