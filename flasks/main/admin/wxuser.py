from flask import request, jsonify
from flask_login import login_required

from . import admin
from .. import admin_required
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
    js = {"data": data, "total_number": wxuser.pages}
    return jsonify(js)
