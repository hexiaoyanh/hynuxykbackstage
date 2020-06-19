from . import admin
from flask_login import login_required


@admin.route('/query_bill/<int:page>')
@login_required
def query_bill(page):
    pass
