import os

from flask import request, jsonify
from flask_login import login_required, current_user

from . import admin
from .. import admin_required, db
from ..models import WXUser


@admin.route('/query_wxuser')
@login_required
@admin_required
def query_wxuser():
    pages = request.args.get('pages')
    num = request.args.get('num')
    wxuser = WXUser.query.paginate(int(pages), int(num))
    data = []
    for i in wxuser.items:
        data.append({
            "id": i.id,
            "userid": i.userid,
            "password": i.password,
            "openid": i.openid,
            "nickname": i.nicename,
            "sex": i.sex,
            "province": i.province,
            "city": i.city,
            "country": i.country,
            "server_expire": i.server_expire,
            "is_subnotice": i.is_subnotice,
            "notification_status": i.notification_status,
            "is_admin": i.is_admin
        })
    return jsonify({"data": data, "total_number": wxuser.pages})


@admin.route('/query_wxuser_by_userid')
@login_required
@admin_required
def query_wxuser_by_userid():
    userid = request.args.get('userid')
    wxuser = WXUser.query.filter(WXUser.userid == userid).first()
    if wxuser is None:
        return jsonify({
            "code": -1,
            "msg": "没有找到此用户"
        })
    return jsonify({
        "id": wxuser.id,
        "userid": wxuser.userid,
        "password": wxuser.password,
        "openid": wxuser.openid,
        "nickname": wxuser.nicename,
        "sex": wxuser.sex,
        "province": wxuser.province,
        "city": wxuser.city,
        "country": wxuser.country,
        "server_expire": wxuser.server_expire,
        "is_subnotice": wxuser.is_subnotice,
        "notification_status": wxuser.notification_status,
        "is_admin": wxuser.is_admin
    })


# 添加某人为管理员
@admin.route('/change_admin_status')
@login_required
@admin_required
def set_admin():
    id = request.args.get()
    if current_user.userid != os.getenv('admin_userid'):
        return jsonify({
            "code": -1,
            "msg": "冒得权限"
        })
    user = WXUser.query.get(id)
    if user is None:
        return jsonify({
            "code": -1,
            "msg": "没有这个id"
        })
    user.is_admin = not user.is_admin
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "设置成功"
    })
