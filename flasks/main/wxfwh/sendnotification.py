import json
import time

import requests

from main import get_access_token
from .. import celery
from .. import access_token


@celery.task()
def send_request(data):
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token.get_access_token(),
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers).json()
    if res.get('errcode') != 0:
        print('==============error:' + res.get('errmsg') + '==============')
    return res


def send_success_sub(openid, out_trade_no, total_fee, time_end):
    # 发生成功订阅通知
    data = {
        "touser": openid,
        "template_id": "oY4cP55QkDeSHiUUV9oGt-_A3oTRnUkSHRjguU1SnxE",
        "data": {
            "first": {
                "value": "上课提醒订阅成功！(*^▽^*)",
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
            },
            "remark": {
                "value": "蟹蟹老板♪(･ω･)ﾉ",
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_class_notification(openid, classname, location, teacher=None, time=None, remark='(〃＞皿＜)'):
    data = {
        "touser": openid,
        "template_id": "fyxZENvUVm7b2elEY3kplBg0Pn5Q4rFQeYM3VIp5xpM",
        "data": {
            "first": {
                "value": "您有一节课将在30分钟后开始Σ(⊙▽⊙\"a",
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
            },
            "remark": {
                "value": remark,
                "color": "173177"
            }
        }
    }
    send_request.delay(data)


def send_exam_notification(openid, exam_name, exam_score):
    data = {
        "touser": openid,
        "template_id": "PCGL1m4dn5JR7U_ydFEBr13kXpQerTt6kXxbe5FqccI",
        "data": {
            "first": {
                "value": "您有一节课的成绩粗来惹(#^.^#)",
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
                "value": "继续加油，奥利给！ヾ(◍°∇°◍)ﾉﾞ",
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_bind_notification(openid, userid):
    data = {
        "touser": openid,
        "template_id": "nlIhlbTT7jUYM_inJdhsSlGDw2HonDCGggxDf5Fq9QU",
        "data": {
            "first": {
                "value": "你的教务网账号已绑定成功，如有成绩出来将在一个小时内会发送通知给你啦ヾ(◍°∇°◍)ﾉﾞ",
                "color": "#173177"
            },
            "keyword1": {
                "value": userid,
                "color": "#173177"
            },
            "keyword2": {
                "value": time.strftime('%Y.%m.%d', time.localtime(time.time())),
                "color": "#173177"
            },
            "remark": {
                "value": "绑定成功还可以订阅上课通知哦(*^▽^*)ﾞ",
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_donate_notification(msg):
    data = {
        "touser": "ovtKGs1iMFFTTClFSQtRmfqsIkt0",
        "template_id": "VVhOVUrytNSKvJXn6rrV3i3rlwWHF8KBFuOMJlBsoSY",
        "data": {
            "first": {
                "value": "有人捐赠了",
                "color": "#173177"
            },
            "keyword1": {
                "value": "有人捐赠了",
                "color": "#173177"
            },
            "keyword2": {
                "value": time.strftime('%Y.%m.%d', time.localtime(time.time())),
                "color": "#173177"
            },
            "remark": {
                "value": msg,
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_ad_notification(userid, username):
    data = {
        "touser": "ovtKGs1iMFFTTClFSQtRmfqsIkt0",
        "template_id": "VVhOVUrytNSKvJXn6rrV3i3rlwWHF8KBFuOMJlBsoSY",
        "data": {
            "first": {
                "value": userid,
                "color": "#173177"
            },
            "keyword1": {
                "value": username,
                "color": "#173177"
            },
            "keyword2": {
                "value": time.strftime('%Y.%m.%d', time.localtime(time.time())),
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_update_notifications(userid, msg, url):
    data = {
        "touser": "ovtKGs185Ka5r0deXTE5Lhqlwrrg",
        # "touser": "ovtKGs1iMFFTTClFSQtRmfqsIkt0",
        "template_id": "xBsPkbbbPM244-IGJ-kA1Bk09jUQT9wqukSAjCUOL08",
        "url": url,
        "data": {
            "first": {
                "value": msg,
                "color": "#173177"
            },
            "keyword1": {
                "value": userid,
                "color": "#173177"
            },
            "keyword2": {
                "value": time.strftime('%Y.%m.%d', time.localtime(time.time())),
                "color": "#173177"
            }
        }
    }
    send_request.delay(data)


def send_start_school_notifications(userid, time_msg, remark_msg, url):
    data = {
        "touser": userid,
        "template_id": "56OyEcjUN8w8bL4_j-98FH2gXXTUwDR-VlRLyfnxYiw",
        "url": url,
        "data": {
            "first": {
                "value": "具体消息请查看衡阳师范学院官方微信公众号",
                "color": "#173177"
            },
            "keyword1": {
                "value": "衡师学子",
                "color": "#173177"
            },
            "keyword2": {
                "value": "衡师服务小助手",
                "color": "#173177"
            },
            "keyword3": {
                "value": time_msg,
                "color": "#173177"
            },
            "keyword4": {
                "value": "衡阳师范学院",
                "color": "#173177"
            },
            "remark": {
                "value": remark_msg,
                "color": "#173177"
            },
        }
    }
    send_request.delay(data)
