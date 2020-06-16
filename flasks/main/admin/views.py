from flask import request, jsonify

from . import admin


@admin.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] != 'admin':
        return jsonify({
            "Code": -1,
            "Msg": "登录失败"
        })
    import os
    if data['password'] != os.getenv('adminpassword'):
        return jsonify({
            "Code": -1,
            "Msg": "登录失败"
        })

