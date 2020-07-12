import requests


# 教务网数据获取
class verifyjw:
    @staticmethod
    def isuseriright(userid, password):
        if userid[0] == 'N':
            res = requests.get(url="http://59.51.24.41/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
        else:
            res = requests.get(
                url="http://59.51.24.46/hysf/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
        if res['msg'] == '账号未启用':
            return "账号未启用"
        if res['flag'] == "1":
            return res
        else:
            return False

    @staticmethod
    def login(userid, password):
        if userid[0] == 'N':
            res = requests.get(url="http://59.51.24.41/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
            return res['token']
        else:
            res = requests.get(
                url="http://59.51.24.46/hysf/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
            return res['token']

    @staticmethod
    def getclass(token, userid, xn, week):
        if userid[0] is 'N':
            token = verifyjw.login('N17080403', '128149')
        else:
            token = ""
        headers = {
            "token": token
        }
        if userid[0] is 'N':
            res = requests.get(
                url="http://59.51.24.41/app.do?method=getKbcxAzc&xh=" + userid + "&xnxqid=" + xn + "&zc=" + week,
                headers=headers).json()
        else:
            res = requests.get(
                url="http://59.51.24.46/hysf/app.do?method=getKbcxAzc&xh=" + userid + "&xnxqid=" + xn + "&zc=" + week,
                headers=headers).json()
        return res

    @staticmethod
    def get_exam(token, userid, xn):
        if userid[0] is 'N':
            token = verifyjw.login('N17080403', '128149')
        else:
            token = ""
        headers = {
            "token": token
        }
        if userid[0] is 'N':
            res = requests.get(
                url="http://59.51.24.41/app.do?method=getCjcx&xh=" + userid + "&xnxqid=" + xn,
                headers=headers).json()
        else:
            res = requests.get(
                url="http://59.51.24.46/hysf/app.do?method=getCjcx&xh=" + userid + "&xnxqid=" + xn,
                headers=headers).json()
        return res
