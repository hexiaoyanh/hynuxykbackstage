from urllib.parse import quote

from flask import jsonify

from . import admin
import uuid
from .data_cache import Data_Cache

data_cache = Data_Cache()


@admin.route('/get_qr_code')
def get_qr_code():
    generate_code = uuid.uuid4()
    data_cache.push(generate_code)
    url1 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri="
    url2 = "&response_type=code&scope=snsapi_userinfo&state=admin_login#wechat_redirect"
    redirect_url = "https://www.hynuxyk.club/wxfwh/admin/login/" + str(generate_code)
    redirect_url = quote(redirect_url, 'utf-8')
    return jsonify({
        "code": 1,
        "url": url1 + redirect_url + url2,
        "generate_code": generate_code
    })


@admin.route('/login/<string:generate_code>')
def login(generate_code):
    pass


@admin.route('/is_login/<string:generate_code>')
def is_login(generate_code):
    pass
