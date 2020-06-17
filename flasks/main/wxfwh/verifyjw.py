import requests


class verifyjw:
    @staticmethod
    def isuseriright(userid, password):
        if userid[0] == 'N':
            res = requests.get(url="http://59.51.24.41/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
        else:
            res = requests.get(
                url="http://59.51.24.46/hysf/app.do?method=authUser&xh=" + userid + "&pwd=" + password).json()
        if res['flag'] == "1":
            return True
        else:
            return False

    @staticmethod
    def getclass(userid, password, week):
        if userid[0] == 'N':
            pass
