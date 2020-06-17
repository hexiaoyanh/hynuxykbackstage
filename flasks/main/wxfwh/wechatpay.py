import time

import requests
import xmltodict
from flask import jsonify, request

from . import wxfwh
from flask_login import login_required

from .pay_settings import random_str, APP_ID, MCH_ID, CREATE_IP, NOTIFY_URL, API_KEY, get_sign, trans_dict_to_xml, \
    trans_xml_to_dict


@wxfwh.route('/createsubpay/<string:openid>')
@login_required
def createsubpay(openid):
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
        'trade_type': 'JSAPI',  # 扫码支付类型
        'openid': openid
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
    data = xmltodict.parse(request.data)
    
    return "ok"
