from flask import Blueprint

admin = Blueprint('/admin', __name__)

from . import bill, curriculum, user, wxuser, views, other_settings
