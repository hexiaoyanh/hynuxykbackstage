from flask import request, jsonify

from . import admin
from flask_login import login_required

from main import admin_required
from main.models import Bill, WXUser


@admin.route('/query_bill')
@login_required
@admin_required
def query_bill():
    page = request.args.get('pages')
    num = request.args.get('num')
    bills = Bill.query.paginate(int(page), int(num))
    data = []
    for i in bills.items:
        data.append({
            "transaction_id": i.transaction_id,
            "out_trade_no": i.out_trade_no,
            "total_fee": i.total_fee,
            "result_code": i.result_code,
            "openid": i.openid,
            "create_time": i.create_time
        })
    js = {'data': data, "total_number": bills.pages}
    return jsonify(js)


@admin.route('/query_bill_by_userid')
@login_required
@admin_required
def query_bill_by_userid():
    userid = request.args.get('userid')
    user = WXUser.query.filter(WXUser.userid == userid).first()
    if user is None:
        return jsonify({
            "code": -1,
            "msg": "没有找到这个用户"
        })
    bill = Bill.query.filter(Bill.openid == user.openid).all()
    data = {}
    for i in bill:
        data[i.transaction_id] = {
            "out_trade_no": i.out_trade_no,
            "total_fee": i.total_fee,
            "result_code": i.result_code,
            "openid": i.openid
        }
    return jsonify(data)
