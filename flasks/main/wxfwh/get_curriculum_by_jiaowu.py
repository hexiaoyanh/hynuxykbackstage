from main.sdk.hynuxykSpider.api.jwlogin import jwlogin
from main.sdk.hynuxykSpider.api.querykb import querykb


class get_curriculum_by_jiaowu:

    def _login(self):
        user = jwlogin(self.userid, self.password, self.nanyue)
        user.login()
        self.cookie = user.cookie
        print(self.cookie)

    def _getkb(self):
        kb = querykb(self.cookie, self.nanyue)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password
        self.nanyue = userid[0] == 'N'
