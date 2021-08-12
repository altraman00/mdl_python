# -*- coding: UTF-8 -*-

import csv
import datetime
import json
from itertools import groupby

import pandas as pd


# 获取区间内的日期
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y/%m/%d")
    date = beginDate[:]
    while date <= endDate:
        # dates.append((str(date),))
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y/%m/%d")
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
        for record in records:
            hiit_email = record['hiit_email']

            recorded_date = record['recorded_date']

            # 格式化
            t_date = datetime.datetime.strptime(recorded_date, "%Y/%m/%d")
            s_date = t_date.strftime("%Y/%m/%d")

            reach_standard = record['reach_standard']
            # print(str(hiit_email) + '---' + str(s_date) + '---' + str(reach_standard))

            record_map[s_date] = reach_standard
        user_record_list.append(record_map)

    return user_record_list


def pd_write_csv(new_csv_path, record_list):
    # 指定需要展示的日期列
    whole_column_names = dateRange('2021/07/23', '2021/08/11')
    # 在列表前面添加邮箱的title
    whole_column_names.insert(0, 'hiit_email')

    final_df = pd.DataFrame(record_list).reindex(whole_column_names, axis=1, fill_value=None)
    print(final_df)
    final_df.to_csv(new_csv_path, mode='a', index=False)


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
    # read_csv_path = 'learn_python/operate_office/resources/hiit达标数据20210812.csv'
    # new_csv_path  = 'learn_python/operate_office/resources/hiit达标数据20210812_deal.csv'

    read_csv_path = '/Users/knight/Desktop/mobvoi/hiit/查询hiit相关达标数据20210812.csv'
    new_csv_path = '/Users/knight/Desktop/mobvoi/hiit/查询hiit相关达标数据20210812_deal.csv'

    # 读取原始的excel并计算相关的结果
    record_list = pd_read_csv(read_csv_path)
    # print(record_list)
    user_record_list = deal_data(record_list)

    json_res = json.dumps(user_record_list, cls=NpEncoder)
    print(json_res)

    whole_column_names = dateRange('2021/07/14', '2021/08/12')
    print(whole_column_names)

    pd_write_csv(new_csv_path, user_record_list)
