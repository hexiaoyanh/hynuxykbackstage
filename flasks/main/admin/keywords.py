from flask import request, jsonify
from flask_login import login_required

from . import admin
from .. import admin_required, db
from ..models import Keywords


@admin.route('/query_keyword')
@login_required
@admin_required
def query_keyword():
    pages = request.args.get('pages')
    num = request.args.get('num')
    keywords = Keywords.query.paginate(int(pages), int(num))
    data = []
    for i in keywords.items:
        data.append({
            "id": i.id,
            "keyword": i.keyword,
            "reply": i.reply
        })
    return jsonify({'data': data, 'total_number': keywords.pages})


@admin.route('/set_keyword', methods=['POST'])
@login_required
@admin_required
def set_keyword():
    data = request.get_json()
    keyword = Keywords.query.filter(Keywords.keyword == data['keyword']).first()
    if keyword is None:
        keyword = Keywords(keyword=data['keyword'], reply=data['reply'])
        db.session.add(keyword)
        db.session.commit()
        return jsonify({
            "code": 1,
            "msg": "添加成功"
        })
    keyword.reply = data['reply']
    db.session.add(keyword)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "修改成功"
    })


@admin.route('/delete_keyword')
@login_required
@admin_required
def delete_keyword():
    id = request.args.get('id')
    keyword = Keywords.query.filter(Keywords.id == id).first()
    if keyword is None:
        return jsonify({
            "code": -1,
            "msg": "id不存在"
        })
    db.session.delete(keyword)
    db.session.commit()
    return jsonify({
        "code": 1,
        "msg": "删除成功"
    })
