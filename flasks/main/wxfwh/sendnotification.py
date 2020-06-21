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
                "value": str(int(total_fee) * 0.01),
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


def send_class_notification(openid, classname, location, teacher=None, time=None):
    data = {
        "touser": openid,
        "template_id": "fyxZENvUVm7b2elEY3kplBg0Pn5Q4rFQeYM3VIp5xpM",
        "data": {
            "first": {
                "value": "您有一节课将在30分钟后开始",
                "color": "#173177"
            },
            "keyword1": {
                "value": classname,
                "color": "#173177"
            },
            "keyword2": {
                "value": location if location is not None else "无",
                "color": "#173177"
            },
            "keyword3": {
                "value": teacher if teacher is not None else "无",
                "color": "#173177"
            },
            "keyword4": {
                "value": time,
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


def send_exam_notification(openid, exam_name, exam_score):
    data = {
        "touser": openid,
        "template_id": "PCGL1m4dn5JR7U_ydFEBr13kXpQerTt6kXxbe5FqccI",
        "data": {
            "first": {
                "value": "您有一节课的成绩粗来了",
                "color": "#173177"
            },
            "keyword1": {
                "value": exam_name,
                "color": "#173177"
            },
            "keyword2": {
                "value": exam_score,
                "color": "#173177"
            },
            "remark": {
                "value": "继续加油，奥利给！",
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
