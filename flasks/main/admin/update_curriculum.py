from main import nowdates, db
from main.models import Curriculum
from main.verifyjw import verifyjw


class Update_curriculum:

    def _getclass(self, userid, password):

        # 使用nowdates的app上下文防止
        with nowdates.app.app_context():
            try:
                token = verifyjw.login(userid, password)
                nowtime = nowdates.get()
                for i in range(25):
                    kecheng = verifyjw.getclass(token, userid, nowtime['xn'], str(i))
                    for j in kecheng:
                        if j is None: continue
                        curriculum = Curriculum.query.filter_by(userid=userid, school_year=nowtime['xn'], week=i,
                                                                class_time=j['kcsj'],
                                                                class_name=j['kcmc'], teacher=j['jsxm'],
                                                                location=j['jsmc'],
                                                                begintime=j['kssj'], endtime=j['jssj'],
                                                                cycle=j['kkzc']).first()
                        if curriculum is not None: continue
                        curriculum = Curriculum(userid=userid, school_year=nowtime['xn'], week=i, class_time=j['kcsj'],
                                                class_name=j['kcmc'], teacher=j['jsxm'], location=j['jsmc'],
                                                begintime=j['kssj'], endtime=j['jssj'], cycle=j['kkzc'])
                        db.session.add(curriculum)
                db.session.commit()
            except Exception as e:
                print("错误:", e)

    def update_class(self, useres):
        self.lens = len(useres)
        self.is_running = True
        for i in useres:
            if i.userid is None:continuel
            self._getclass(i.userid, i.password)
            self.now_run += 1
        self.is_running = False
        self.lens = 0
        self.now_run = 0

    def is_running(self):
        if self.is_running:
            return True
        return False

    # 获取当前进度
    def get_schedule(self):
        import math
        if self.is_running:
            return math.floor(self.now_run / self.lens * 100)
        else:
            return 0

    def __init__(self):
        self.is_running = False
        self.lens = 0
        self.now_run = 0
