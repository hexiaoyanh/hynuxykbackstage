# 微信支付配置
# ========支付相关配置信息===========
import random
import time
import hashlib
from random import Random
import os

APP_ID = os.getenv('appid')  # 你公众账号上的appid
MCH_ID = "1600291052"  # 你的商户号
API_KEY = os.getenv('api_key')  # 微信商户平台(pay.weixin.qq.com) -->账户设置 -->API安全 -->密钥设置，设置完成后把密钥复制到这里
APP_SECRECT = os.getenv('wx_appsecret')
UFDODER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"  # 该url是微信下单api
NOTIFY_URL = "https://www.hynuxyk.club/wxfwh/successpay"  # 微信支付结果回调接口，需要改为你的服务器上处理结果回调的方法路径
CREATE_IP = '106.15.249.85'  # 你服务器的IP


def get_sign(data_dict, key):
    """
    签名函数
    :param data_dict: 需要签名的参数，格式为字典
    :param key: 密钥 ，即上面的API_KEY
    :return: 字符串
    """
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    print(params_list)
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign


def order_num(phone):
    """
    生成扫码付款订单号
    :param phone: 手机号
    :return:
    """
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    result = phone + 'T' + local_time + random_str(5)
    return result


def random_str(randomlength=8):
    """
    生成随机字符串
    :param randomlength: 字符串长度
    :return:
    """
    strs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        strs += chars[random.randint(0, length)]
    return strs


def trans_dict_to_xml(data_dict):
    """
    定义字典转XML的函数
    :param data_dict:
    :return:
    """
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml))  # 返回XML


def trans_xml_to_dict(data_xml):
    """
    定义XML转字典的函数
    :param data_xml:
    :return:
    """
    import xmltodict
    return xmltodict.parse(data_xml)
