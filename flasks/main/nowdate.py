import datetime
import time


# 计算当前学期和周数
class nowdate:
    year = None
    month = None
    day = None

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def init_app(self, app):
        self.app = app

    def get(self):
        a = datetime.date(self.year, self.month, self.day).isocalendar()
        b = datetime.datetime.now().isocalendar()
        if self.month <= 7:
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
