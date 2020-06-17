import json

import requests

from main import get_access_token


def send_success_sub(openid, out_trade_no, total_fee, time_end):
    # 发生成功订阅通知
    data = {
        "touser": openid,
        "template_id": "oY4cP55QkDeSHiUUV9oGt-_A3oTRnUkSHRjguU1SnxE",
        "data": {
            "first": {
                "value": "上课提醒订阅成功！",
                "color": "#173177"
            },
            "keyword1": {
                "value": out_trade_no,
                "color": "#173177"
            },
            "keyword2": {
                "value": total_fee,
                "color": "#173177"
            },
            "keyword3": {
                "value": "衡师服务小助手",
                "color": "#173177"
            },
            "keyword4": {
                "value": time_end,
                "color": "#173177"
            }
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    access_tokens = get_access_token()
    res = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_tokens.get_access_token(),
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers).json()
    print(res)
    return res
