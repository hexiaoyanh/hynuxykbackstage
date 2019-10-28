from flask import Blueprint

query = Blueprint('/query', __name__)

from . import views
