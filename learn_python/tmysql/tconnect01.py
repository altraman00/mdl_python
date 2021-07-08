# -*- coding: UTF-8 -*-

"""
python connect mysql
"""
import os
import json
import pymysql

host = "localhost"
user = "root"
password = "123456"
database = "motion-health-statistics"


def db_conn():
    str = """
            {
              "host": "localhost",
              "port": 3306,
              "user": "root",
              "password": "123456",
              "db": "motion-health-statistics",
              "charset": "utf8"
              }
        """
    # mysql_conf = {'host': '10.0.0.0', 'port': 3306, 'user': 'dev', 'password': 'sctele@dev', 'db': 'test', 'charset': 'utf8'}
    mysql_conf = json.loads(str, encoding='utf-8')
    try:
        connect = pymysql.Connect(**mysql_conf)
    except Exception as err:
        raise err
    return connect


# 批量插入mysql
def many_insert_mysql(dbconnect,sql,rows):
    try:
        cursor = dbconnect.cursor()
        if rows:
            print(sql)
            print(rows)
            cursor.executemany(sql, rows)
    finally:
        dbconnect.commit()
        cursor.close()


if __name__ == '__main__':

    fields = ['num1', 'num2']
    sql = """INSERT INTO tt ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )

    rows = []
    for num in range(2):
        sql_ = sql % (num, num)
        print('--->' + sql_)
        row_single = []
        row_single.append(num)
        row_single.append(num)
        rows.append(row_single)

    # 3.连接数据库
    with db_conn() as dbconnect:
        many_insert_mysql(dbconnect,sql,rows)
