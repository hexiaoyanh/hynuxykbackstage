from flask import Blueprint

wxfwh = Blueprint('/wxfwp', __name__)

from . import views, subnotice
