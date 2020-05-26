"""
@File : __init__.py.py
@Author: Mika
@Date : 2020/4/7
@Desc :
"""
from flask import Blueprint

publicexam = Blueprint('/publicexam', __name__)

from . import views

