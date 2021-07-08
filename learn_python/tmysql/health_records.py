# -*- coding: UTF-8 -*-

"""
python connect mysql
"""
import json

import requests

from python_mdl.car.car_licence.config.logger_config import get_logger
import python_mdl.tmysql.basemodule as baseMd

logger = get_logger(log_file_path='./log/ticwatch.log')


def saveMotionRecords(wwid, motion_records):
    fields = ['account_id', 'type', 'start_at', 'end_at', 'total_distance', 'total_calorie', 'total_steps',
              'total_motion_time', 'avg_heart_rate', 'recorded_at']
    sql = """INSERT INTO tb_motion_records ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )
    rows = []
    for item in motion_records:
        obj = []
        # account_id = item['account_id']
        type = item['type']
        start_at = item['start_at']
        end_at = item['end_at']
        total_distance = item['total_distance']
        total_calorie = item['total_calorie']
        total_steps = item['total_steps']
        total_motion_time = item['total_motion_time']
        avg_heart_rate = item['avg_heart_rate']
        recorded_at = item['timestamp']

        obj.append(baseMd.md5ByWwid(wwid))
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

    # 连接数据库并保存
    with baseMd.db_conn() as dbconnect:
        baseMd.many_insert_mysql(dbconnect, sql, rows)


def saveHealthRecords(wwid, data_type, health_records):
    fields = ['account_id', 'type', 'start_at', 'end_at']
    sql = """INSERT INTO tb_health_records ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )
    rows = []
    obj = []
    start_at = health_records['min_start_time_ms']
    end_at = health_records['max_end_time_ms']

    obj.append(baseMd.md5ByWwid(wwid))
    obj.append(data_type)
    obj.append(start_at)
    obj.append(end_at)
    print(obj)

    rows.append(obj)

    # 连接数据库并保存
    with baseMd.db_conn() as dbconnect:
        baseMd.many_insert_mysql(dbconnect, sql, rows)


def saveHealthRecordsPoints(wwid, data_type, points):
    fields = ['account_id', 'type', 'start_at', 'end_at', 'val']
    sql = """INSERT INTO tb_health_records_points ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )
    rows = []
    for item in points:
        obj = []
        start_at = item['start_time_millis']
        end_at = item['end_time_millis']
        string_val = item['string_val']

        obj.append(baseMd.md5ByWwid(wwid))
        obj.append(data_type)
        obj.append(start_at)
        obj.append(end_at)
        obj.append(string_val)
        print(obj)

        rows.append(obj)

    # 连接数据库并保存
    with baseMd.db_conn() as dbconnect:
        baseMd.many_insert_mysql(dbconnect, sql, rows)


def saveSleepSessionRecords(wwid, sleep_type, sleep_records):
    fields = ['account_id', 'type', 'start_at', 'end_at']
    sql = """INSERT INTO tb_health_records ({fields}) VALUE ({mark});""".format(
        fields='`' + '`,`'.join(fields) + '`',
        mark=','.join(['%s'] * len(fields))
    )
    rows = []
    obj = []
    start_at = sleep_records['start_time_ms']
    end_at = sleep_records['end_time_ms']

    obj.append(baseMd.md5ByWwid(wwid))
    obj.append(sleep_type)
    obj.append(start_at)
    obj.append(end_at)
    print(obj)

    rows.append(obj)

    # 连接数据库并保存
    with baseMd.db_conn() as dbconnect:
        baseMd.many_insert_mysql(dbconnect, sql, rows)


if __name__ == '__main__':
    motionType = ''
    # users = [
    #     'b39ce9a9b793484e920bdc215510728c', '2e5b17bf0d6449c7a43fc1d75caa6f06',
    #     '7817ab705677467188506a14ef8818c6', '79aa6a854cc54d7cbd9dd3aad6a21854',
    #     'cfafe91725794eab8837a39c30c54dd3', '3a7e7c80e4e745a3a7fc875a9abd7441',
    #     '9605ce174ad24b6685a2f8f0827102da', 'a3623bbe81eb48339503c64a3ecdf2e7',
    #     '6d9dc915861240b68bde59c36781523c', '31070a2b76684fb08d644f9f810ce198'
    # ]

    users = [
        'b03b8bf6d51e5b1ed5b6f38c28425352', '24230db45fc6f9f9ede78a6a3717eae4', '5b15708fc2c24aa0b4f1eadd2fb43f75',
        'a90848ef82aa4f7386a36b8c0b86ef8d', 'd150933b0ad44c5b97497c118b5c0a3a', 'dec6a2f953804eac8925aba4aff9ebb1',
        '460c605b13a9409ab1409f7c4e041385', '7eb67d084ce74fa2a4e0cfacd0dcb809', 'e43215e959764407979f30dcbf5792f4',
        'c6e94ddfee9a413eb27393f31e0f5250', 'b6c9890901fb4c64a87ffd9a411c6267',
        # 'f210d5c53d3f4cdab213d6bebf335e85',
        '21c1b156a8a34e5490d33f31a5b7a63e', '67be6c62d91a47b19e923ed413e7ed70'
    ]

    # users = [
    #     'b39ce9a9b793484e920bdc215510728c'
    # ]

    for wwid in users:
        sessionId = baseMd.getSessionIdByWwid(wwid)

        # # 运动数据
        # records = baseMd.getMotionRecords(sessionId, motionType, 1, 100)
        # logger.info('records:' + json.dumps(records))
        # logger.info('result size=' + str(len(records)))
        # saveMotionRecords(wwid, records)

        # 健康数据
        start_time = 1614528000000
        end_time = 1624607532813

        data_types = ['heart_rate', 'blood_oxygen', 'delta_distance', 'delta_step', 'high_strength_training']

        # for data_type in data_types:
        #     health_records = baseMd.getDataByDataType(sessionId, start_time, end_time, data_type)
        #     print(health_records)
        #     for data_sets in health_records:
        #         # 保存data_session
        #         saveHealthRecords(wwid, data_type, data_sets)
        #         # 保存points
        #         points = data_sets['points']
        #         saveHealthRecordsPoints(wwid, data_type, points)

        # 睡眠数据
        sleep_type = 'sleep_motion'
        sleepSessions = baseMd.getSleepDataSession(sessionId, start_time, end_time)
        for sleep_records in sleepSessions:
            saveSleepSessionRecords(wwid, sleep_type, sleep_records)
            start_time_ms = sleep_records['start_time_ms']
            end_time_ms = sleep_records['end_time_ms']

            sleep_records = baseMd.getDataByDataType(sessionId, start_time_ms, end_time_ms, sleep_type)
            if len(sleep_records) > 0:
                sleep_data_set = sleep_records[0]
                # 保存睡眠points
                sleep_points = sleep_data_set['points']
                print("points")
                saveHealthRecordsPoints(wwid, sleep_type, sleep_points)
