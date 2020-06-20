from urllib.parse import quote

from flask import jsonify, request

from . import admin
import uuid
from .data_cache import Data_Cache

data_cache = Data_Cache()


# 生成二维码链接
@admin.route('/get_qr_code')
def get_qr_code():
    generate_code = uuid.uuid4()
    data_cache.push(generate_code)
    url1 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri="
    url2 = "&response_type=code&scope=snsapi_userinfo&state=admin_login#wechat_redirect"
    redirect_url = "https://www.hynuxyk.club/wx/admin/login/" + str(generate_code)
    redirect_url = quote(redirect_url, 'utf-8')
    return jsonify({
        "code": 1,
        "url": url1 + redirect_url + url2,
        "generate_code": generate_code
    })


# 访问此网址登录
@admin.route('/login/<string:generate_code>')
def login(generate_code):
    status = data_cache.set(generate_code)
    code = request.args.get('code')

    if status is None:
        return jsonify({
            "code": -1,
            "msg": "没有找到此generate_code"
        })
    elif status is False:
        return jsonify({
            "code": -1,
            "msg": "此generate_code已过期，请刷新二维码再重试登录"
        })
    else:
        return jsonify({
            "code": 1,
            "msg": "登录成功"
        })


# 判断是否登录成功
@admin.route('/is_login/<string:generate_code>')
def is_login(generate_code):
    status = data_cache.get(generate_code)
    if status is None:
        return jsonify({
            "code": -1,
            "msg": "没有找到此generate_code"
        })
    elif status is False:
        return jsonify({
            "code": -1,
            "msg": "用户还未扫码"
        })
    elif status == "used":
        return jsonify({
            "code": -1,
            "msg": "错误，此验证码已使用"
        })
    else:
        pass
