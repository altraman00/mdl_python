# -*- coding: UTF-8 -*-

"""
python connect mysql
"""
import json
import sys

import pymysql
import requests
import hashlib

from python_mdl.car.car_licence.config.logger_config import get_logger

host = "localhost"
user = "root"
password = "123456"
database = "motion-health-statistics"

logger = get_logger(log_file_path='./log/ticwatch.log')


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
def many_insert_mysql(dbconnect, sql, rows):
    try:
        cursor = dbconnect.cursor()
        if rows:
            print(sql)
            print(rows)
            cursor.executemany(sql, rows)
    finally:
        dbconnect.commit()
        cursor.close()


def getSessionIdByWwid(wwid):
    url = """http://account.mobvoi.com/token/fork/wwid?wwid={wwid}""".format(wwid=wwid)
    print('url:' + url)
    r = requests.get(url, stream=True)
    print(r.content)
    sessionId = json.loads(r.content)['sub_token']
    if sessionId is None:
        print("wwid错误，获取sessionId失败")
        sys.exit(0)
    return sessionId


# 获取motion_records
def getMotionRecords(sessionId, motionType, pageNo, pageSize):
    url = """https://health.ticwear.com/data/accounts/51129599/records/page/motion?sessionId={sessionId}&motionType={motionType}&pageNo={pageNo}&pageSize={pageSize}""" \
        .format(sessionId=sessionId, motionType=motionType, pageNo=pageNo, pageSize=pageSize)
    r = requests.get(url, stream=True)
    # print(r.content)
    try:
        records = json.loads(r.content)['records']
    except:
        print("解析异常")
    return records


def saveRecords(md5wwid, motion_records):
    fields = ['account_id', 'type', 'start_at', 'end_at', 'total_distance', 'total_calorie', 'total_steps',
              'total_motion_time', 'avg_heart_rate', 'recorded_at']
    sql = """INSERT INTO tb_motion_records ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )

    rows = []
    for item in motion_records:
        obj = []
        account_id = item['account_id']
        type = item['type']
        start_at = item['start_at']
        end_at = item['end_at']
        total_distance = item['total_distance']
        total_calorie = item['total_calorie']
        total_steps = item['total_steps']
        total_motion_time = item['total_motion_time']
        avg_heart_rate = item['avg_heart_rate']
        recorded_at = item['timestamp']

        obj.append(md5wwid)
        obj.append(type)
        obj.append(start_at)
        obj.append(end_at)
        obj.append(0 if total_distance < 0 else total_distance)
        obj.append(0 if total_calorie < 0 else total_calorie)
        obj.append(0 if total_steps < 0 else total_steps)
        obj.append(total_motion_time)
        obj.append(0 if avg_heart_rate < 0 else avg_heart_rate)
        obj.append(recorded_at)
        print(obj)
        print(str(obj))

        rows.append(obj)

    # 3.连接数据库
    with db_conn() as dbconnect:
        many_insert_mysql(dbconnect, sql, rows)


def md5ByWwid(wwid):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(wwid.encode(encoding='utf-8'))
    res = hl.hexdigest()
    print('MD5加密前为 ：' + wwid)
    print('MD5加密后为 ：' + res)
    return res


if __name__ == '__main__':
    # batchSave()

    motionType = ''

    users = [
        'b03b8bf6d51e5b1ed5b6f38c28425352', '24230db45fc6f9f9ede78a6a3717eae4', '5b15708fc2c24aa0b4f1eadd2fb43f75',
        'a90848ef82aa4f7386a36b8c0b86ef8d', 'd150933b0ad44c5b97497c118b5c0a3a', 'dec6a2f953804eac8925aba4aff9ebb1',
        '460c605b13a9409ab1409f7c4e041385', '7eb67d084ce74fa2a4e0cfacd0dcb809', 'e43215e959764407979f30dcbf5792f4',
        'c6e94ddfee9a413eb27393f31e0f5250', 'b6c9890901fb4c64a87ffd9a411c6267',
        # 'f210d5c53d3f4cdab213d6bebf335e85',
        '21c1b156a8a34e5490d33f31a5b7a63e', '67be6c62d91a47b19e923ed413e7ed70'
    ]

    for wwid in users:
        sessionId = getSessionIdByWwid(wwid)
        records = getMotionRecords(sessionId, motionType, 1, 60)
        logger.info('records:' + json.dumps(records))
        logger.info('result size=' + str(len(records)))
        # md5wwid = md5ByWwid(wwid)
        saveRecords(wwid, records)
