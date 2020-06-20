from flask import request, jsonify
from flask_login import login_required

from . import admin

# 设置开学日期
from main import admin_required, nowdates, wechatsettings


@admin.route('/set_time')
@login_required
@admin_required
def set_time():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    nowdates.set(int(year), int(month), int(day))
    return jsonify({
        "code": 1,
        "msg": "开学日期设置成功"
    })


# 获取开学日期
@admin.route('/get_time')
@login_required
@admin_required
def get_time():
    return nowdates.get()


@admin.route('/get_customize_menu')
@login_required
@admin_required
def get_customize_menu():
    return wechatsettings.get_menu()


@admin.route('/set_customize_menu', methods=['POST'])
@login_required
@admin_required
def set_customize_menu():
    data = str(request.data, 'utf-8')
    return jsonify({
        "code": 1,
        "msg": wechatsettings.set_menu(data)
    })


@admin.route('/get_total_fee')
@login_required
@admin_required
def get_total_fee():
    return jsonify({
        "code": 1,
        "total_fee": wechatsettings.get_total_fee()
    })


@admin.route('/set_total_fee')
@login_required
@admin_required
def set_total_fee():
    total_fee = request.args.get('total_fee')
    wechatsettings.set_total_fee(total_fee)
    return jsonify({
        "code": 1,
        "msg": "设置成功"
    })
