# -*- coding: UTF-8 -*-

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.mysql_operator import MySqlOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['xx@163.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    'MySqlOperatorExample',
    default_args=default_args,
    description='MySqlOperatorExample',
    schedule_interval="*/10 * * * *")

insert_sql = "INSERT INTO `test-cloud`.`city`(`id`, `name`, `pid`,`sort`) VALUES (MD5(UUID()), 'zhangsan', 19, 1)"

task = MySqlOperator(
    task_id='select_sql',
    sql=insert_sql,
    mysql_conn_id='mysql_test-cloud',
    autocommit=True,
    dag=dag)

