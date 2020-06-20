import datetime


class Data_Cache():
    token_data = {}

    def _delete_expired_data(self):
        now_time = datetime.datetime.now()
        for i in self.token_data:
            if (now_time - self.token_data[i]['expire_in']).seconds >= 120:
                del i

    def push(self, uuid):
        self._delete_expired_data()
        self.token_data[uuid] = {
            "expire_in": datetime.datetime.now(),
            "is_auth": 0,
            "openid": None
        }
        print(self.token_data)

    def set(self, uuid, openid):
        now_time = datetime.datetime.now()
        print(self.token_data)
        if self.token_data.get(uuid) is None:
            return None
        elif (now_time - self.token_data[uuid]['expire_in']).seconds >= 120:
            return False
        else:
            self.token_data[uuid]['is_auth'] += 1
            if self.token_data[uuid]['is_auth'] >= 2:
                return "used"
            self.token_data[uuid]['openid'] = openid
            return True

    def get(self, uuid):
        print(self.token_data)
        if self.token_data.get(uuid) is None:
            return None
        elif self.token_data[uuid]['is_auth'] == 0:
            return False
        elif self.token_data[uuid]['is_auth'] != 0:
            self.token_data[uuid]['is_auth'] += 1
            if self.token_data[uuid]['is_auth'] > 2:
                return "used"
            return self.token_data[uuid]['openid']
        else:
            return None

    def __init__(self):
        pass
