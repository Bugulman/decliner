import pandas as pd
import oily_report as olr
import pickle
import os

olr.create_report_dir(path=get_project_folder())

print(os.getcwd())
with open('some.pickle', 'rb') as file:
    df = pickle.load(file)


def df_to_table(df: pd.DataFrame, name='from_df'):
    """Функция экспортирует датафрейм в таблицу дизайнера моделей
    name - имя таблицы"""
    create_table(name=name, overwrite_existing=True)
    print(df.shape)
    rows, cols = df.shape
    get_table_by_name(name=name).set_size(
        r_count=rows, c_count=cols)
    for n, col_name in enumerate(df.columns):
        get_table_by_name(name=name).set_column_header(
            column=n+1, text=col_name)
    for row_n, row in enumerate(df.iterrows()):
        for col_n, col in enumerate(row[1]):
            # , col)
            print(
                f'row {row_n+1} col {col_n+1} данные {df.iloc[row_n,col_n]}')
            get_table_by_name(name=name).set_data(
                row=row_n+1, column=col_n+1, data=str(df.iloc[row_n, col_n]))
