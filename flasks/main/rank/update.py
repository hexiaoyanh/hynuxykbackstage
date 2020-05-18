from sql import DBSession, User, yiliu, yiqi, yiba, yijiu
from setvalue import setnumvalue, setavevalue, setgpavalue, setxfvalue

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


def getgrade(xh, xqmc):
    if xh[:2] == "16":
        # return yiliu.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
        return session.query(yiliu).filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "17":
        # return yiqi.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
        return session.query(yiqi).filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "18":
        # return yiba.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
        return session.query(yiba).filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
    elif xh[:2] == "19":
        # return yijiu.query.filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()
        return session.query(yijiu).filter_by(userid=xh, xqmc=xqmc, ksxzmc="正常考试").all()


def deal(i, j, rx):
    xq = "20" + str(j) + "-20" + str(j + 1)
    print(xq)
    grade1 = getgrade(i.xh, xq + "-1")
    shang = 0
    xia = 0
    gpa1 = 0
    gpa2 = 0
    shangxf = 0
    xiaxf = 0

    shanglen = len(grade1)
    if shanglen == 0: return
    for k in grade1:
        if is_contains_chinese(k.zcj):
            cj = rank2grade[k.zcj]
        else:
            cj = float(k.zcj)
        gpa1 += 4 - 3 * (100 - cj) ** 2 / 1600
        shang += cj
        shangxf += float(k.xf)
    i = setnumvalue(i, rx, j, 1, shang)
    i = setgpavalue(i, rx, j, 1, gpa1)
    i = setxfvalue(i, rx, j, 1, shangxf)
    i = setavevalue(i, rx, j, 1, shang / shanglen)
    session.add(i)

    grade2 = getgrade(i.xh, xq + "-2")
    xialen = len(grade2)
    if xialen == 0: return
    for k in grade2:
        if is_contains_chinese(k.zcj):
            cj = rank2grade[k.zcj]
        else:
            cj = float(k.zcj)
        xia += cj
        gpa2 += 4 - 3 * (100 - cj) ** 2 / 1600
        xiaxf += float(k.xf)
    i = setnumvalue(i, rx, j, 2, xia)
    i = setgpavalue(i, rx, j, 2, gpa2)
    i = setxfvalue(i, rx, j, 2, xiaxf)
    i = setavevalue(i, rx, j, 2, xia / xialen)
    session.add(i)


import threading


def cal_num(s):
    user = session.query(User).filter(User.xh.like(s)).all()
    if len(user) == 0: return
    for i in user:
        rx = int(i.xh[:2])
        print(i.xh, i.xm, rx)
        for j in range(rx, 20):
            deal(i, j, rx)
            # p = Process(target=deal, args=(i, j, rx,))
            # thread = threading.Thread(target=deal, args=(i, j, rx,))
            # thread.start()
            # thread.join()
        session.commit()


from multiprocessing import Process


def is_alive(p):
    for i in p:
        if i.is_alive():
            return 0
    return 1


if __name__ == '__main__':
    process_list = []
    flag = 1
    flag1 = True
    flag2 = True
    for x in range(16, 20):
        while True:
            for i in range(flag, flag + 10):
                if flag1 == False: break
                if i <= 9:
                    zy = "0" + str(i)
                else:
                    zy = str(i)
                p = Process(target=cal_num, args=(str(x) + zy + "%",))
                p.start()
                process_list.append(p)

            flag1 = False
            for i in process_list:
                if flag2 == False: break
                i.join()
            flag2 = False

            if is_alive(process_list):
                process_list = []
                flag1 = True
                flag2 = True
                flag += 10

            if flag >= 80: break
