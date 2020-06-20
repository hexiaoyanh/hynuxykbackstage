from flask_login import login_required

from . import admin
from main import admin_required


@admin.route('/query_curriculum')
@login_required
@admin_required
def query_curriculum():
    pass