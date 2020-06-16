import hashlib
import time

import xmltodict as xmltodict
from flask import request, make_response

from . import wxfwh


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
                    "Content": u"哈哈哈哈",
                }
            if response:
                response = {"xml": response}
                response = xmltodict.unparse(response)
            else:
                response = ''
            return make_response(response)
    else:
        return ""


@wxfwh.route('/test')
def test():
    return "ok"
