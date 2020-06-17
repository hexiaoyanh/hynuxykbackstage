from flask import request, jsonify
from . import wxfwh
from flask_login import login_required, current_user
from .verifyjw import verifyjw
from .. import db


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


