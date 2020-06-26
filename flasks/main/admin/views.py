from datetime import datetime
from urllib.parse import quote

from flask import jsonify, request
from flask_login import login_user, login_required, current_user

from . import admin
import uuid
from main import access_token, admin_required, db
from main.models import WXUser, Usern, User, Generate_code


# 生成二维码链接
@admin.route('/get_qr_code')
def get_qr_code():
    generate_code = uuid.uuid4()
    url1 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri="
    url2 = "&response_type=code&scope=snsapi_userinfo&state=admin_login#wechat_redirect"
    redirect_url = "https://www.hynuxyk.club/wx/admin/login/" + str(generate_code)
    redirect_url = quote(redirect_url, 'utf-8')
    # 删掉过期的code
    now_time = datetime.now()
    allcode = Generate_code.query.all()
    for i in allcode:
        if (now_time - i.exipre_in).seconds > 300:
            db.session.delete(i)
    db.session.add(Generate_code(generate_code=str(generate_code), exipre_in=datetime.now()))
    db.session.commit()
    return jsonify({
        "code": 1,
        "url": url1 + redirect_url + url2,
        "generate_code": str(generate_code)
    })


# 访问此网址登录
@admin.route('/login')
def login():
    generate_code = request.args.get('generate_code')
    code = request.args.get('code')
    res = access_token.code2access_token(code)
    if res.get('errcode') is not None:
        return jsonify({
            "code": "-1",
            "msg": res['errmsg']
        })
    token = Generate_code.query.filter(Generate_code.generate_code == generate_code).first()
    now_time = datetime.now()  # 如果不存到变量里会出问题，我也不知道为什么
    print(now_time, token.exipre_in)
    if token is None:
        return jsonify({
            "code": -1,
            "msg": "该generate_code已失效"
        })
    elif (now_time - token.exipre_in).seconds > 120:
        db.session.delete(token)
        db.session.commit()
        return jsonify({
            "code": -1,
            "msg": "该验证码已过期"
        })
    else:
        token.openid = res['openid']
        token.is_auth = True
        db.session.add(token)
        db.session.commit()
        return jsonify({
            "code": 1,
            "msg": "登录成功"
        })


# 判断是否登录
@admin.route('/is_logins')
def is_logins():
    if current_user.is_authenticated:
        return jsonify({'code': 1})
    else:
        return jsonify({'code': -1})


# 判断是否登录成功
@admin.route('/is_login/<string:generate_code>')
def is_login(generate_code):
    code = Generate_code.query.filter(Generate_code.generate_code == generate_code).first()
    if code is None:
        return jsonify({
            "code": -2,
            "msg": "该generate_code不存在"
        })
    elif code.is_auth is False:
        return jsonify({
            "code": -1,
            "msg": "该generate_code还未验证"
        })
    elif code.is_auth is True:
        user = WXUser.query.filter(WXUser.openid == code.openid).first()
        if user.is_admin is False:
            return jsonify({
                "code": -2,
                "msg": "您没有权限"
            })
        login_user(user)
        return jsonify({
            "code": 1,
            "msg": "登录成功"
        })


# 通过openid查询用户信息
@admin.route('/openid2user/<string:openid>')
# @login_required
# @admin_required
def openid2user(openid):
    user = WXUser.query.filter(WXUser.openid == openid).first()
    if user is None:
        return jsonify({
            "code": -1,
            "msg": "此用户不存在"
        })
    if user.userid is None:
        return jsonify({
            "code": -1,
            "msg": "此用户未绑定教务网"
        })
    if user.userid[0] == 'N':
        users = Usern.query.filter(Usern.xh == user.userid).first()
    else:
        users = User.query.filter(User.xh == user.userid).first()
    if users is None:
        return jsonify({
            "code": -1,
            "msg": "其他错误"
        })
    return jsonify({
        "code": 1,
        "userid": users.xh,
        "class_name": users.bj,
        "name": users.xm,
        "phone_number": users.dh
    })
