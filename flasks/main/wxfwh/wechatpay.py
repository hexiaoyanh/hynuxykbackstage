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
from .verifyjw import verifyjw
from .. import db, nowdates
from ..models import WXUser, Curriculum, Bill


@wxfwh.route('/createsubpay')
@login_required
def createsubpay():
    nonce_str = random_str()  # 拼接出随机的字符串即可，我这里是用 时间+随机数字+5个随机字母
    total_fee = 1  # 付款金额，单位是分，必须是整数
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
    print(xml)
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
                    openid=['openid'])
        db.session.add(bill)
        nowtime = datetime.datetime.now()
        if nowtime.month < 7:
            nowtime = datetime.datetime(nowtime.year, nowtime.month + 6, nowtime.day)
        else:
            nowtime = datetime.datetime(nowtime.year + 1, nowtime.month + 6 - 12, nowtime.day)

        if user.is_subnotice:
            GetClass(user.userid, user.password)

        user.server_expire = nowtime
        user.is_subnotice = True
        db.session.add(user)
        db.session.commit()
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"


def GetClass(userid, password):
    from manage import app
    thr = threading.Thread(target=getclass, args=[app, userid, password, ])  # 创建线程
    thr.start()


def getclass(app, userid, password):
    with app.app_context():
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
                                                            begintime=j['kssj'], endtime=j['jssj'],
                                                            cycle=j['kkzc']).first()
                    if curriculum is not None: continue
                    curriculum = Curriculum(userid=userid, school_year=nowtime['xn'], week=i, class_time=j['kcsj'],
                                            class_name=j['kcmc'], teacher=j['jsxm'], location=j['jsmc'],
                                            begintime=j['kssj'], endtime=j['jssj'], cycle=j['kkzc'])
                    db.session.add(curriculum)
            db.session.commit()
        except Exception as e:
            print("错误:", e)
