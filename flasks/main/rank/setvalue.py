from sql import DBSession, User


def setnumvalue(user, rx, j, xq, value):
    if rx == j:
        if xq == 1:
            user.dayi_shang_num = value
        else:
            user.dayi_xia_num = value
    elif j - rx == 1:
        if xq == 1:
            user.daer_shang_num = value
        else:
            user.daer_xia_num = value
    elif j - rx == 2:
        if xq == 1:
            user.dasan_shang_num = value
        else:
            user.dasan_xia_num = value
    elif j - rx == 3:
        if xq == 1:
            user.dasi_shang_num = value
        else:
            user.dasi_xia_num = value
    return user


def setgpavalue(user, rx, j, xq, value):
    if rx == j:
        if xq == 1:
            user.dayi_shang_gpa = value
        else:
            user.dayi_xia_gpa = value
    elif j - rx == 1:
        if xq == 1:
            user.daer_shang_gpa = value
        else:
            user.daer_xia_gpa = value
    elif j - rx == 2:
        if xq == 1:
            user.dasan_shang_gpa = value
        else:
            user.dasan_xia_gpa = value
    elif j - rx == 3:
        if xq == 1:
            user.dasi_shang_gpa = value
        else:
            user.dasi_xia_gpa = value
    return user


def setxfvalue(user, rx, j, xq, value):
    if rx == j:
        if xq == 1:
            user.dayi_shang_xf = value
        else:
            user.dayi_xia_xf = value
    elif j - rx == 1:
        if xq == 1:
            user.daer_shang_xf = value
        else:
            user.daer_xia_xf = value
    elif j - rx == 2:
        if xq == 1:
            user.dasan_shang_xf = value
        else:
            user.dasan_xia_xf = value
    elif j - rx == 3:
        if xq == 1:
            user.dasi_shang_xf = value
        else:
            user.dasi_xia_xf = value
    return user


def setavevalue(user, rx, j, xq, value):
    if rx == j:
        if xq == 1:
            user.dayi_shang_ave = value
        else:
            user.dayi_xia_ave = value
    elif j - rx == 1:
        if xq == 1:
            user.daer_shang_ave = value
        else:
            user.daer_xia_ave = value
    elif j - rx == 2:
        if xq == 1:
            user.dasan_shang_ave = value
        else:
            user.dasan_xia_ave = value
    elif j - rx == 3:
        if xq == 1:
            user.dasi_shang_ave = value
        else:
            user.dasi_xia_ave = value
    return user
