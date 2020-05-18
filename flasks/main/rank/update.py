from sql import DBSession, User, yiliu, yiqi, yiba, yijiu
from setvalue import setnumvalue, setavevalue, setgpavalue, setxfvalue
from sqlfunc import create_table_is_not_exists, insert_data

session = DBSession()

rank2grade = {
    "优": 95,
    "良": 85,
    "中": 75,
    "及格": 60,
    "合格": 60,
    "不及格": 0,
    "通过": 60
}


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def migrate(nj):
    grade = session.query(nj).all()
    for i in grade:
        print(i.userid, i.xm)
        table_name = str(i.userid[:4])
        create_table_is_not_exists(table_name)
        data = {
            "userid": i.userid,
            "bz": i.bz,
            "cjbsmc": i.cjbsmc,
            "kclbmc": i.kclbmc,
            "zcj": i.zcj,
            "xm": i.xm,
            "xqmc": i.xqmc,
            "kcxzmc": i.kcxzmc,
            "ksxzmc": i.ksxzmc,
            "kcmc": i.kcmc,
            "xf": i.xf,
            "bj": i.bj
        }
        insert_data(table_name, data)


from multiprocessing import Process

if __name__ == '__main__':
    pross = []
    p = Process(target=migrate, args=(yiqi,))
    p.start()
    pross.append(p)
    p = Process(target=migrate, args=(yiba,))
    p.start()
    pross.append(p)
    p = Process(target=migrate, args=(yijiu,))
    p.start()
    pross.append(p)
    for i in pross:
        i.join()
