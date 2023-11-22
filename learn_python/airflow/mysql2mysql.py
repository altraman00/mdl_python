# -*- coding: UTF-8 -*-

import time
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.hooks import mysql_hook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # "start_date": datetime(2021, 11, 23),
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG('mysql_mysql_crm',
          default_args=default_args,
          schedule_interval="*/5 * * * *")

def write_to_mysql(**kwargs):
    """
    将mysql获取的数据写入新的mysql
    :param kwargs:
    :return:
    """

    mysql_hook_A = mysql_hook.MySqlHook("mysql_test-cloud")    # mysql_A 连接id
    mysql_hook_B = mysql_hook.MySqlHook("mysql_test-cloud-2")  # mysql_B 连接id

    sql_ora = """
            SELECT
                md5( uuid( ) ) AS id,
                count( 1 ) AS `name`,
                FLOOR( 500 + RAND( ) * 100 ) AS pid,
                FLOOR( 1 + RAND( ) * 100 ) sort 
            FROM
                city t;
            """


    conn_oracle = mysql_hook_A.get_conn()
    conn_mysql = mysql_hook_B.get_conn()


    cur = conn_oracle.cursor()
    mys_cur = conn_mysql.cursor()
    mys_cur.execute('SET autocommit = 0')
    try:
        cur.execute(sql_ora)
        rs = cur.fetchall()
        for line in rs:
            time_ = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            id = line[0]
            name = line[1]
            pid = line[2]
            sort = line[3]
            sql_mys = "insert into city (id,`name`,pid,sort) value ('%s','%s',%d,%d)" % (id, name, pid, sort)
            mys_cur.execute(sql_mys)


    except Exception as e:
        sql_del = "delete from city where create_date='%s'" % time_
        mys_cur.execute(sql_del)
        conn_mysql.rollback()
        raise e
    conn_mysql.commit()
    cur.close()
    conn_oracle.close()
    mys_cur.close()
    conn_mysql.close()


with dag:
    t1 = PythonOperator(python_callable=write_to_mysql, task_id="write_mysql")
    t2 = DummyOperator(task_id="dummy")

t1 >> t2
