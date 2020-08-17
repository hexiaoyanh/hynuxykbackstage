import json

import requests

from . import access_token


class WechatSetting:
    # 设置微信菜单
    total_fee = 1
    data = None

    def _load_menu(self):
        with open('menu.json', 'r') as f:
            self.data = json.loads(f.read())

    def _save_menu(self):
        with open('menu.json', 'w') as f:
            f.write(json.dumps(self.data))

    def _setmenu(self):
        self._load_menu()
        access_tokens = access_token.get_access_token()
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(url="https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_tokens,
                            headers=headers, data=json.dumps(self.data, ensure_ascii=False).encode('utf-8')
                            ).json()
        print("自定义菜单:", res['errmsg'])
        return res['errmsg']

    def get_menu(self):
        self._load_menu()
        return self.data

    def set_menu(self, data):
        self.data = data
        self._setmenu()
        return self._save_menu()

    def set_total_fee(self, total_fee):
        self.total_fee = total_fee
        with open('total_fee', 'w') as f:
            f.write(str(total_fee))

    def get_total_fee(self):
        with open('total_fee', 'r') as f:
            return int(f.read())

    def __init__(self):
        self._setmenu()
        pass

    def init_app(self, app):
        self.app = app
