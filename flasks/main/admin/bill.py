from flask import request, jsonify

from . import admin
from flask_login import login_required

from main import admin_required
from main.models import Bill


@admin.route('/query_bill')
@login_required
@admin_required
def query_bill():
    psge = request.args.get('pages')
    num = request.args.get('num')
    bills = Bill.query.paginate(int(psge), int(num))
    data = {}
    for i in bills:
        data[i.transaction_id] = {
            "out_trade_no": i.out_trade_no,
            "total_fee": i.total_fee,
            "result_code": i.result_code,
            "openid": i.openid
        }
    return jsonify(data)

