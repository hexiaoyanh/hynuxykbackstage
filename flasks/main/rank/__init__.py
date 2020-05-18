from flask import Blueprint

rank = Blueprint('/rank', __name__)

from . import view