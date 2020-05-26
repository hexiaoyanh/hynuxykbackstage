"""
@File : __init__.py.py
@Author: Mika
@Date : 2019/12/23
@Desc :
"""
from flask import Blueprint

submsg = Blueprint('/submsg', __name__)

from . import views
