from flask import request, jsonify
from . import wxfwh
from flask_login import login_required, current_user
from .verifyjw import verifyjw
from .. import db
from ..models import Curriculum


@wxfwh.route('/bindjw', methods=['POST'])
@login_required
def bindjw():
    data = request.get_json()
    if verifyjw.isuseriright(data['userid'], data['password']):
        current_user.userid = data['userid']
        current_user.password = data['password']
        db.session.add(current_user)
        db.session.commit()
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
        db.session.delete(curriculum)
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
