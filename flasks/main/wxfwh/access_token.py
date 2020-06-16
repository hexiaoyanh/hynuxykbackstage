import json
import time

import requests

from flasks.config import Config


# 一个获取微信access_token的插件
class get_access_token:
    access_token = None
    time = None

    def __init__(self):
        pass

    def init_app(self, app):
        self.app = app
        self._update_access_token()

    def _update_access_token(self):
        params = {
            "grant_type": "client_credential",
            "appid": Config.appid,
            "secret": Config.wx_appsecret
        }
        res = requests.get(url="https://api.weixin.qq.com/cgi-bin/token", params=params)
        res = json.loads(res.text)
        self.access_token = res['access_token']
        self.time = time.time()

    # 判断是否过期
    def _is_expired(self):
        nowtime = time.time()
        if nowtime - self.time >= 7000:
            return True
        return False

    def get_access_token(self):
        if self._is_expired():
            self._update_access_token()
        return self.access_token
