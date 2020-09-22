import re

from .hynuxykSpider.api.jwlogin import jwlogin
from .hynuxykSpider.api.querykb import querykb
import json


def convert_key_to_time(s):
    s = s.split('-')
    if s[0] == '1':
        return "08:30"
    elif s[0] == '2':
        return "10:30"
    elif s[0] == '3':
        return "14:30"
    elif s[0] == '4':
        return "16:30"
    elif s[0] == '5':
        return "19:30"


class get_curriculum_from_jiaowu:
    def login(self):
        self.user = jwlogin(username=self.userid, password=self.password, nanyue=(self.userid[0] == 'N'))

    def get_curriculum(self, week):
        curriculum = querykb(self.user.cookie["JSESSIONID"], nanyue=(self.userid[0] == 'N'))
        return curriculum.queryallkb(self.now_time, week)

    # 转化课表信息为msg
    def convert_curriculum2json(self, week):
        kb = json.loads(self.get_curriculum(week))
        all = []
        for i in kb:
            class_name = list(i[0].values())[0]
            times = str(list(i[1].keys())[0])  # 获取时间日期
            msg = list(i[1].values())[0]
            if msg == '': continue
            # 将多余的空格转成一个并且分开
            msg = msg[len(class_name):]
            # 有些班级比较离谱，课程名里有空格
            msg = re.sub(r'\s+', ' ', msg).split(' ')
            all.append({
                "class_time": convert_key_to_time(times),
                "class_day": times[2],
                "class_name": class_name,
                "teacher": msg[2],
                "location": msg[4],
                "week": week
            })
        return all

    def get_all(self):
        all = []
        for i in range(1, 21):
            all.append(self.convert_curriculum2json(str(i)))
        return all

    def __init__(self, userid, password, now_time):
        self.userid = userid
        self.password = password
        self.now_time = now_time
        self.login()
