"""
@File : views.py
@Author: Mika
@Date : 2019/12/23
@Desc :
"""

from flask import request
import requests
from . import submsg


@submsg.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json()
    openid = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid=wx87b2e9598df82c7d&secret=408ca1e3e3bd2f1b3d75b93befc64de0&js_code=' +
            data['code'] + '&grant_type=authorization_code')
    print(openid.text)
    return openid.text
