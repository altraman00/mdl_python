# -*- coding: UTF-8 -*-

import json
import sys

import pymysql
import requests
import hashlib

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


def md5ByWwid(wwid):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(wwid.encode(encoding='utf-8'))
    res = hl.hexdigest()
    print('MD5加密前为 ：' + wwid)
    print('MD5加密后为 ：' + res)
    return res


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


# 获取data_set数据
def getDataByDataType(token, start_time, end_time, data_type):
    url = """https://fitness.mobvoi.com/v1/users/me/data-sources/derived:com.mobvoi.fitness/data-sets/{start_time} - {end_time}?data_type={data_type}""" \
        .format(start_time=start_time, end_time=end_time, data_type=data_type)
    header = {
        'token': token
    }
    r = requests.get(url, headers=header, stream=True)
    try:
        records = json.loads(r.content)['data_sets']
    except:
        print("datasets解析异常")
    return records

#
def getSleepDataSession(token, start_time, end_time):
    url = """https://fitness.mobvoi.com/v1/users/me/data-sources/derived:com.mobvoi.fitness/data-sessions/{start_time} - {end_time}?data_type=auto_sleep""" \
        .format(start_time=start_time, end_time=end_time)
    header = {
        'token': token
    }
    r = requests.get(url, headers=header, stream=True)
    try:
        records = json.loads(r.content)['data_sessions']
    except:
        print("dataSessions解析异常")
    return records