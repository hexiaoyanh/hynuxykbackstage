from flask import Blueprint

donate = Blueprint('/donate', __name__)

from . import views
