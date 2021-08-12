# -*- coding: UTF-8 -*-
import datetime

import pandas as pd


# 参考：
# 通过将列名与字典匹配来填充dataframe中的值
# https://www.5axxw.com/questions/content/n9358w

def demo1():
    export_dict = [
        {'Chat': 1, 'Email': 4, 'VM': 15, 'web': 10},
        {'Chat': 3, 'Email': 6, 'Phone': 2, 'VM': 15},
        {'Email': 5, 'Phone': 4, 'VM': 7, 'Year': 1},
    ]
    whole_title = ['Chat', 'Email', 'Phone', 'VM', 'web', 'Sum', 'Year']

    final_df = pd.DataFrame(export_dict).reindex(whole_title, axis=1, fill_value=None)
    print(final_df)

    new_csv_path = '/Users/knight/Desktop/mobvoi/hiit/demo2.csv'
    final_df.to_csv(new_csv_path, mode='a', index=False)


def demo2():
    export_dict = [
        {'email': 'xxx@163.com', '2021-08-01': '1', '2021-08-03': '3', '2021-08-06': '6'},
        {'email': 'yyy@163.com', '2021-08-02': 2, '2021-08-05': 5, '2021-08-09': 9},
        {'email': 'zzz@163.com', '2021-08-05': 5, '2021-08-07': 7, '2021-08-11': 11},
    ]
    whole_title = ['2021-08-01', '2021-08-02', '2021-08-03', '2021-08-04', '2021-08-05',
                   '2021-08-06', '2021-08-07', '2021-08-08', '2021-08-09', '2021-08-10', '2021-08-11']

    final_df = pd.DataFrame(export_dict).reindex(whole_title, axis=1, fill_value=None)
    print(final_df)

    new_csv_path = '/Users/knight/Desktop/mobvoi/hiit/demo2.csv'
    final_df.to_csv(new_csv_path, mode='a', index=False)


if __name__ == '__main__':
    # demo1()
    demo2()
