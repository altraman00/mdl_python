# -*- coding: UTF-8 -*-
import pandas as pd

# List of Tuples
students = [
    ('Ankit'),
    ('Swapnil'),
    ('Priya'),
    ('Shivangi'),
]

# Create a DataFrame object
stu_df = pd.DataFrame(students, columns=['Name'], index=['1'])

# Iterate over column names
for column in stu_df:
    # Select column contents by column
    # name using [] operator
    columnSeriesObj = stu_df[column]
    print('Colunm Name : ', column)
    print('Column Contents : ', columnSeriesObj.values)
stu_df.to_csv(r"/Users/knight/Desktop/mobvoi/hiit/csv_hiit_2.csv", mode='a', index=False)
