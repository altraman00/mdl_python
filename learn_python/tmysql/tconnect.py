# -*- coding: UTF-8 -*-

import pymysql

# 打开数据库连接
db = pymysql.connect(host="localhost", user="root", password="123456", database="motion-health-statistics")

# 使用cursor()方法获取操作游标
cursor = db.cursor()
insert_sql = "INSERT INTO `motion-health-statistics`.`stream_motion_statistics_day`(`id`, `statistical_date`, `wwid`, `account_id`, `region`, `gender`, `type`, `total_distance`, `total_calorie`, `total_steps`, `total_motion_time`, `avg_heart_rate`, `swim_pool_length`, `swim_trips`, `swim_distance`, `swim_stroke`, `created_at`, `updated_at`) " \
             "VALUES (md5(uuid())1, '2020-01-05', '12528ab3e7988f370deea8e4af133c8d', 29706383, 'Japan', '0', 0, 561544, 571561, 55151, 167751, 46, 0, 0, 0, 0, '2021-02-10 12:25:31', '2021-02-10 12:25:31');"

try:
    # 执行sql语句
    cursor.execute(insert_sql)
    # 提交到数据库执行
    db.commit()
    cursor.execute("select * from stream_motion_statistics_day")
    # 查看表里所有数据
    data = cursor.fetchall()
    print(data)
except Exception as e:
    print("数据插入失败,请查检try语句里的代码" + e)

# 关闭数据库连接
# 如果想知道报了啥错,可以主动抛出异常
# raise
db.close()
