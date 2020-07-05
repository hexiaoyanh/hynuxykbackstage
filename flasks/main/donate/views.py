import os
import time

import requests
import xmltodict
from flask import request, jsonify

from . import donate
from .. import db
from ..models import Donate
from ..wxfwh.pay_settings import random_str, MCH_ID, CREATE_IP, API_KEY, get_sign, trans_dict_to_xml, trans_xml_to_dict
from ..wxfwh.sendnotification import send_donate_notification


@donate.route('/code2session')
def code2session():
    code = request.args.get('code')
    print(code)
    params = {
        "appid": os.getenv('mini_id'),
        "secret": os.getenv('mini_secret'),
        "js_code": code,
        "grant_type": "grant_type"
    }
    res = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=params).json()

    return res['openid']


@donate.route('/donate', methods=['POST'])
def donates():
    money = request.get_json()['money']
    openid = request.get_json()['openid']
    nonce_str = random_str()  # 拼接出随机的字符串即可，我这里是用 时间+随机数字+5个随机字母
    params = {
        'appid': os.getenv('mini_id'),  # APPID
        'mch_id': MCH_ID,  # 商户号
        'nonce_str': nonce_str,  # 随机字符串
        'out_trade_no': random_str(),  # 订单编号，可自定义
        'total_fee': int(money) * 100,  # 订单总金额
        'spbill_create_ip': CREATE_IP,  # 自己服务器的IP地址
        'notify_url': "https://www.hynuxyk.club/donate/success_donate",  # 回调地址，微信支付成功后会回调这个url，告知商户支付结果
        'body': '衡师小助手小程序',  # 商品描述
        'detail': '捐赠',  # 商品描述
        'trade_type': 'JSAPI',  # jsapi支付类型
        'openid': openid
    }
    sign = get_sign(params, API_KEY)  # 获取签名
    params['sign'] = sign  # 添加签名到参数字典
    xml = trans_dict_to_xml(params)  # 转换字典为XML
    response = requests.post(url="https://api.mch.weixin.qq.com/pay/unifiedorder", data=xml.encode("utf-8"))
    data_dict = trans_xml_to_dict(response.content)['xml']  # 将请求返回的数据转为字典
    params = {}
    params['appId'] = os.getenv('mini_id')
    params['timeStamp'] = int(time.time())
    params['nonceStr'] = random_str(16)
    params['package'] = 'prepay_id=' + data_dict['prepay_id']
    params['signType'] = 'MD5'
    params['paySign'] = get_sign({'appId': os.getenv('mini_id'),
                                  "timeStamp": params['timeStamp'],
                                  'nonceStr': params['nonceStr'],
                                  'package': 'prepay_id=' + data_dict['prepay_id'],
                                  'signType': 'MD5',
                                  },
                                 API_KEY)

    return jsonify(params)


@donate.route('/success_donate', methods=['POST'])
def success_donate():
    data = xmltodict.parse(request.data)['xml']
    print(data)
    if data['result_code'] == 'SUCCESS':
        donate = Donate.query.filter(Donate.openid == data['openid']).first()
        if donate is None:
            donate = Donate(openid=data['openid'], fee=int(data['total_fee']))
        else:
            donate.fee += int(data['total_fee'])
        db.session.add(donate)
        db.session.commit()
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"


@donate.route('/update_user_info', methods=['POST'])
def update_user_info():
    data = request.get_json()
    send_donate_notification(data['msg'])
    donate = Donate.query.filter(Donate.openid == data['openid']).first()
    donate.message = data['msg']
    donate.name = data['name']
    db.session.add(donate)
    db.session.commit()
    return "非常非常感谢您的捐赠"


@donate.route('/get_user_list')
def get_user_list():
    donate = Donate.query.all()
    lists = []
    for i in donate:
        js = {
            "no": i.id,
            "name": i.name,
            "num": i.fee
        }
        lists.append(js)
    return jsonify(lists)
