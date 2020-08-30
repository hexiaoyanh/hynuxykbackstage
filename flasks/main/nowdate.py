import datetime
import json
import time


# 计算当前学期和周数
class nowdate:
    year = None
    month = None
    day = None

    def __init__(self, year, month, day):
        with open('nowdates', 'r') as f:
            js = json.loads(f.read())
            self.year = js['year']
            self.month = js['month']
            self.day = js['day']

    def set(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        with open('nowdates', 'w') as f:
            f.write(json.dumps({
                "year": year,
                "month": month,
                "day": day
            }))

    def init_app(self, app):
        self.app = app

    def _get(self):
        with open('nowdates', 'r') as f:
            js = json.loads(f.read())
            self.year = js['year']
            self.month = js['month']
            self.day = js['day']

    def get_begin_time(self):
        self._get()
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day
        }

    def get(self):
        self._get()
        a = datetime.date(self.year, self.month, self.day).isocalendar()
        b = datetime.datetime.now().isocalendar()
        if 8 >= self.month >= 2:
            return {
                "xn": str(self.year - 1) + '-' + str(self.year) + '-' + '2',
                'week': b[1] - a[1]
            }
        else:
            c = datetime.date(self.year, 12, 31).isocalendar()

            if c[1] - a[1] > b[1] - a[1]:
                return {
                    "xn": str(self.year) + '-' + str(self.year + 1) + '-' + '1',
                    'week': (c[1] - a[1]) + b[1]
                }
            else:
                return {
                    "xn": str(self.year) + '-' + str(self.year + 1) + '-' + '1',
                    'week': b[1] - a[1]
                }
