import json
import math
import os
import time

import requests


# 一个获取微信access_token的插件


class get_access_token:
    access_token = None
    time = None

    def __init__(self):
        pass

    def _update_access_token(self):
        params = {
            "grant_type": "client_credential",
            "appid": os.getenv('appid'),
            "secret": os.getenv('wx_appsecret')
        }
        res = requests.get(url="https://api.weixin.qq.com/cgi-bin/token", params=params)
        res = json.loads(res.text)
        try:
            self.access_token = res['access_token']
            self.time = time.time()
            with open('/tmp/access_token.json', 'w') as f:
                f.write(json.dumps({"access_token": res['access_token'], "time": math.floor(self.time)}))
        except KeyError as e:
            print("access_token error:", e)

    # 判断是否过期
    def _is_expired(self):
        nowtime = time.time()
        try:
            with open('/tmp/access_token.json', 'r') as f:
                try:
                    js = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    self._update_access_token()
                self.access_token = js['access_token']

                if nowtime - int(js['time']) >= 7000:
                    return True
                return False
        except FileNotFoundError:
            self._update_access_token()

    def get_access_token(self):
        if self._is_expired():
            self._update_access_token()
        return self.access_token

    def code2access_token(self, code):
        params = {
            "appid": os.getenv('appid'),
            "secret": os.getenv('wx_appsecret'),
            "code": code,
            "grant_type": "authorization_code"
        }
        res = requests.get(url="https://api.weixin.qq.com/sns/oauth2/access_token", params=params)
        res = json.loads(res.text)
        return res
