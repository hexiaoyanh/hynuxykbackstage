import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="03190319",
    database="grade"
)


# 判断表是否存在，不存在则创建
def create_table_is_not_exists(table_name):
    sql = "create table if not exists `grade_{}`(\
    `id` int not null auto_increment primary key,\
    `userid` varchar(64) not null,\
    `bz` varchar(64),\
    `cjbsmc` varchar(64),\
    `kclbmc` varchar(64),\
    `zcj` varchar(64),\
    `xm` varchar(64),\
    `xqmc` varchar(64),\
    `kcxzmc` varchar(64),\
    `ksxzmc` varchar(64),\
    `kcmc` varchar(64),\
    `xf` varchar(10),\
    `bj` varchar(64));".format(table_name)
    mycursor.execute(sql)


# 插入数据
def insert_data(table_name, data):
    sql = "insert into grade_{} (userid, bz, cjbsmc, kclbmc, zcj, xm, xqmc, kcxzmc, ksxzmc, kcmc, xf, bj) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(
        table_name)
    value = (
        data['userid'],
        data['bz'],
        data['cjbsmc'],
        data['kclbmc'],
        data['zcj'],
        data['xm'],
        data['xqmc'],
        data['kcxzmc'],
        data['ksxzmc'],
        data['kcmc'],
        data['xf'],
        data['bj'])
    mycursor.execute(sql, value)
    mydb.commit()


# 查询数据
def select_data(mycursor, table_name, userid, xqmc):
    sql = "select * from grade_{} where userid=%s and xqmc=%s and (kclbmc='必修' or kclbmc='任选' or kclbmc='限选')".format(
        table_name)
    value = (userid, xqmc)
    rows = mycursor.session.execute(sql, value).fetchall()
    print(rows)
    return rows

# if __name__ == '__main__':
#     print(select_data("1601", "16010101", "2017-2018-1")[0])
