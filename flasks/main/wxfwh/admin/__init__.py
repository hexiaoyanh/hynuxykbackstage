from flask import Blueprint

admin = Blueprint('/wxfwh/admin', __name__)

from . import bill, curriculum, grade, user, wxuser, views
