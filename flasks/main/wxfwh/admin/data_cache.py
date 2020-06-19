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
            "is_auth": False
        }

    def get(self, uuid):
        self._delete_expired_data()
        if self.token_data.get(uuid) is None:
            return None
        elif not self.token_data[uuid]['is_auth']:
            return False
        elif self.token_data[uuid]['is_auth']:
            return True
        else:
            return None

    def __init__(self):
        pass
