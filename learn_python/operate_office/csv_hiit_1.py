# -*- coding: UTF-8 -*-

import csv
import datetime
import json
from itertools import groupby

import pandas as pd


# 获取区间内的日期
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        # dates.append((str(date),))
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


# 循环写列
def write_columns(csv_path, column_names):
    print(column_names)
    data = pd.DataFrame(columns=column_names)
    # mode=a，以追加模式写入
    data.to_csv(csv_path, mode='a', index=False)


# 读取csv文件获取数据
def pd_read_csv(csv_path):
    data = pd.read_csv(csv_path)
    # print(type(data))
    record_list = []
    for i in range(len(data)):
        user_date_count_dict = {}
        document = data[i:i + 1]
        hiit_email = document['hiit_email'][i]
        recorded_date = document['recorded_date'][i]
        reach_standard = document['reach_standard'][i]
        # print(str(hiit_email) + '--' + str(recorded_date) + '--' + str(reach_standard))
        user_date_count_dict['hiit_email'] = hiit_email
        user_date_count_dict['recorded_date'] = recorded_date
        user_date_count_dict['reach_standard'] = reach_standard
        record_list.append(user_date_count_dict)
    return record_list


def deal_data(record_list):
    sex_group = groupby(record_list, key=lambda x: (x["hiit_email"]))
    user_record_list = []
    for key, group in sex_group:
        # unit_data = json.dumps(list(group), cls=NpEncoder)
        # print(key, unit_data)

        email = key
        records = list(group)
        print(email, records)

        record_map = {'hiit_email': email}
        record_dates = []
        record_reach_standard_counts = []
        for record in records:
            hiit_email = record['hiit_email']
            recorded_date = record['recorded_date']
            reach_standard = record['reach_standard']
            # print(str(hiit_email) + '---' + str(recorded_date) + '---' + str(reach_standard))
            record_dates.append(recorded_date)
            record_reach_standard_counts.append(reach_standard)

        record_map['reach_standard_counts'] = record_reach_standard_counts
        record_map['record_dates'] = record_dates
        user_record_list.append(record_map)
    return user_record_list


def pd_write_csv(new_csv_path, record_list):
    for record in record_list:
        val_email = (record['hiit_email'],)
        val_count = tuple(record['reach_standard_counts'])
        titles = record['record_dates']
        val = val_email + val_count
        unit_data = [val]
        titles.insert(0, 'email')
        print(unit_data)
        print(titles)
        data = pd.DataFrame(unit_data, columns=titles)
        data.to_csv(new_csv_path, mode='a', index=False)


def read_csv(csv_path):
    range = dateRange('2018-02-01', '2018-03-10')

    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        rows = csv.reader(csv_file)

        # 去重的邮箱
        email_list = []
        user_date_count_dic = {}

        for row in rows:
            # print(type(row))
            content = row[0] + '--->' + row[1] + '--->' + row[2]
            # print(content)
            email = row[0]
            count = row[1]
            date = row[2]
            if email not in email_list:
                email_list.append(email)
                user_date_count_dic['email'] = email
            else:
                user_date_count_dic['email']

    print(len(email_list))


def write_csv_1(csv_path):
    dates = dateRange('2018-02-01', '2018-03-10')
    with open(csv_path, "wt", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in dates:
            print(row)
            # 使用元组()才会导致数字不分割
            writer.writerow((str(row),))


def write_csv_2():
    # date = dateRange('2018-02-01', '2018-03-10')
    data = pd.read_csv(r'/Users/knight/Desktop/mobvoi/hiit/查询hiit相关达标数据的副本.csv')  # 打开一个csv，得到data对象
    print(data.columns)  # 获取列索引值
    data1 = data['date']  # 获取name列的数据
    data[data1] = data1  # 将数据插入新列new
    # 保存到csv,  mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    data.to_csv(r"/Users/knight/Desktop/mobvoi/hiit/csv_hiit_1.csv", mode='a', index=False)
    print(data)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.np.integer):
            return int(obj)
        elif isinstance(obj, pd.np.floating):
            return float(obj)
        elif isinstance(obj, pd.np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


if __name__ == '__main__':
    read_csv_path = '/Users/knight/Desktop/mobvoi/hiit/查询hiit相关达标数据.csv'
    new_csv_path = '/Users/knight/Desktop/mobvoi/hiit/csv_hiit_1.csv'

    # 指定需要展示的日期列
    column_names = dateRange('2021-07-14', '2021-08-11')
    # 在列表前面添加邮箱的title
    column_names.insert(0, 'email')
    print(column_names)
    # 先写入列
    write_columns(new_csv_path, column_names)

    # 读取原始的excel并计算相关的结果
    record_list = pd_read_csv(read_csv_path)
    # print(record_list)
    user_record_list = deal_data(record_list)

    json_res = json.dumps(user_record_list, cls=NpEncoder)
    print(json_res)

    pd_write_csv(new_csv_path, user_record_list)
