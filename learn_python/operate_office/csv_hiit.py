# -*- coding: UTF-8 -*-

import csv
import datetime


# 获取区间内的日期
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def read_csv(csv_path):
    range = dateRange('2018-02-01', '2018-03-10')

    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        rows = csv.reader(csv_file)

        # 去重的邮箱
        email_list = []
        for row in rows:
            # print(type(row))
            content = row[0] + '--->' + row[1] + '--->' + row[2]
            print(content)
            email = row[0]
            count = row[1]
            date = row[2]
            if email not in email_list:
                email_list.append(email)

    print(len(email_list))


def write_csv_1(path):
    dates = dateRange('2018-02-01', '2018-03-10')
    with open(path, "wt", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in dates:
            print(row)
            # 使用元组()才会导致数字不分割
            writer.writerow((str(row),))

def write_csv_2(path):
    dates = dateRange('2018-02-01', '2018-03-10')
    with open(path, 'w', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for aa in dates:
            filewriter.writerow([aa])
            for phrase in dates:
                filewriter.writerow([phrase])


if __name__ == '__main__':
    csv_path = '/Users/knight/Desktop/mobvoi/hiit/csv_hiit.csv'
    # read_csv(csv_path)
    # write_csv_1(csv_path)
    write_csv_2(csv_path)
