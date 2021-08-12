# -*- coding: UTF-8 -*-
import pandas as pd

# List of Tuples
students = [
    ('Ankit', 22, 'A'),
    ('Swapnil', 22, 'B'),
    ('Priya', 22, 'B'),
    ('Shivangi', 22, 'B'),
]

# Create a DataFrame object
stu_df = pd.DataFrame(students, columns=['Name', 'Age', 'Section'], index=['1', '2', '3', '4'])

# Iterate over column names
for column in stu_df:
    # Select column contents by column
    # name using [] operator
    columnSeriesObj = stu_df[column]
    print('Colunm Name : ', column)
    print('Column Contents : ', columnSeriesObj.values)
stu_df.to_csv(r"/Users/knight/Desktop/mobvoi/hiit/csv_hiit_2.csv", mode='a', index=False)
