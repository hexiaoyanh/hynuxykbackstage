import requests
from flask import request, jsonify
from . import wxfwh
from flask_login import login_required, current_user
from main.verifyjw import verifyjw
from .sendnotification import send_bind_notification
from .. import db, nowdates
from ..models import Curriculum


@wxfwh.route('/bindjw', methods=['POST'])
@login_required
def bindjw():
    data = request.get_json()
    if data['userid'] is None or data['password'] is None:
        return jsonify({
            "code": -1,
            "msg": "请输入账号或密码"
        })
    try:
        res = verifyjw.isuseriright(data['userid'], data['password'])
    except requests.exceptions.ConnectionError:
        return jsonify({
            "code": -1,
            "msg": "教务网暂时不可能访问，请稍后再试"
        })
    if res is not False or res == "账号未启用":
        current_user.userid = data['userid']
        current_user.password = data['password']
        db.session.add(current_user)
        db.session.commit()
        send_bind_notification(current_user.openid, data['userid'])
        return jsonify({
            "code": 1,
            "msg": "绑定成功"
        })
    else:
        return jsonify({
            "code": -1,
            "msg": "账号或密码错误"
        })


@wxfwh.route('/isbindjw')
@login_required
def is_bind_jw():
    if current_user.userid is None:
        return jsonify({
            "code": -1,
            "msg": "没有绑定教务系统"
        })
    else:
        return jsonify({
            "code": 1,
            "msg": "已经绑定了教务系统",
            "userid": current_user.userid
        })


@wxfwh.route('/cancel_bind_jw')
@login_required
def cancel_bind_jw():
    if current_user.userid is None:
        return jsonify({
            "code": 1,
            "msg": "您没有绑定教务网"
        })
    else:
        curriculum = Curriculum.query.filter(Curriculum.userid == current_user.userid).all()
        for i in curriculum:
            db.session.delete(i)
        current_user.userid = None
        current_user.password = None
        current_user.is_subnotice = False
        db.session.add(current_user)
        db.session.commit()
        db.session.add(current_user)
        db.session.commit()
        return jsonify({
            "code": 1,
            "msg": "已取消绑定教务网"
        })


