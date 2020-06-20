import datetime


class Data_Cache():
    token_data = {}

    def _delete_expired_data(self):
        now_time = datetime.datetime.now()
        for i in self.token_data:
            if (now_time - i['expire_in']).seconds >= 120:
                del i

    def push(self, uuid):
        self.token_data[uuid] = {
            "expire_in": datetime.datetime.now(),
            "is_auth": 0
        }

    def set(self, uuid):
        now_time = datetime.datetime.now()
        if self.token_data.get(uuid) is None:
            return None
        elif (now_time - self.token_data['expire_in']).seconds >= 120:
            return False
        else:
            self.token_data[uuid]['is_auth'] += 1
            return True

    def get(self, uuid):
        if self.token_data.get(uuid) is None:
            return None
        elif not self.token_data[uuid]['is_auth'] == 0:
            return False
        elif self.token_data[uuid]['is_auth'] != 0:
            self.token_data[uuid]['is_auth'] += 1
            if self.token_data[uuid]['is_auth'] > 2:
                return "used"
            return True
        else:
            return None

    def __init__(self):
        pass
