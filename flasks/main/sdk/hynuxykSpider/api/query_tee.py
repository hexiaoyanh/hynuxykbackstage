import requests


class Query_tee:
    session = requests.Session()

    def _get_verify_code(self):
        url = "http://fszj.czt.hunan.gov.cn/wap/randomCodeServlet/getCode.htm?action=loadImg&token=159714680496951465276"
        try:
            res = self.session.get(url=url, timeout=5)
            print(res.content)
            print(res.cookies)
        except requests.exceptions.Timeout:
            return {
                "code": -1,
                "msg": "请求超时"
            }

    def __init__(self, userid):
        self.userid = userid
        self._get_verify_code()


if __name__ == '__main__':
    query_tee = Query_tee('17690208')
