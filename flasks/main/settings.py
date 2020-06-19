import json

import requests

from . import access_token


class WechatSetting:
    # 设置微信菜单
    total_fee = 1

    def _setmenu(self):
        data = {
            "button": [
                {
                    "type": "click",
                    "name": "订阅通知",
                    "key": "classinfo",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "绑定教务网",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri=https%3A%2F%2Fwww.hynuxyk.club%2Fwx/&response_type=code&scope=snsapi_userinfo&state=bindjw#wechat_redirect"
                        },
                        {
                            "type": "view",
                            "name": "订阅上课通知",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri=https%3A%2F%2Fwww.hynuxyk.club%2Fwx/&response_type=code&scope=snsapi_userinfo&state=submsg#wechat_redirect"
                        }
                    ]
                },
                {
                    "type": "miniprogram",
                    "name": "小程序",
                    "pagepath": "pages/index/index",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri=https%3A%2F%2Fwww.hynuxyk.club%2Fwx/&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect",
                    "appid": "wx064b82571d2be21f"
                },
                {
                    "name": "课程表",
                    "sub_button": [
                        {
                            "type": "miniprogram",
                            "name": "课表小程序",
                            "pagepath": "pages/class/class",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3f45ab7ab0b12aed&redirect_uri=https%3A%2F%2Fwww.hynuxyk.club%2Fwx/&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect",
                            "appid": "wx365d77f700333956"

                        }]
                }]
        }
        access_tokens = access_token.get_access_token()
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(url="https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_tokens,
                            headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8')
                            ).json()
        print("自定义菜单:", res['errmsg'])

    def get_total_fee(self):
        return self.total_fee

    def __init__(self):
        pass

    def init_app(self, app):
        self.app = app
        self._setmenu()
