import pandas as pd
import numpy as np
import sqlalchemy
from slugify import slugify
import calendar
from pandas.tseries.offsets import MonthBegin
import os


def frame_to_psql(df, con_str, table_name):
    """функция для экспорта таблицы в БД
    df-DataFrame для загрузки
    con_str-строка для подключения вида
    table_name-имя таблицы в БД
    'postgresql://test:test@localhost:5434/test'"""
    engine = sqlalchemy.create_engine(
        con_str)
    df.to_sql(name=table_name, con=engine)


def worked_time(frame, delta=0):
    """Добавляет столбец с временем работы"""
    frame["Time"] = frame["date"] - frame["date"].min()
    frame["Time"] = frame["Time"] / np.timedelta64(1, "D")
    frame["Time"] = frame["Time"] + delta
    return frame


def day_in_month(i):
    """Количество дней в дате i - дата"""
    return calendar.monthrange(i.year, i.month)[1]


def montly_dob(frame, summ_list=['QOIL', 'QWAT', 'QLIQ', 'QWIN', 'SQOIL', 'SQLIQ']):
    """Добавляет столбецы с ежемесячной и накопленной добычей к датафрейму"""
    for i in summ_list:
        name = 'MON'+i
        name2 = 'SUMM'+i
        frame[name] = frame['date'].apply(day_in_month)*frame[i]*frame['WEFA']
        frame[name2] = frame[name].cumsum()/1000
    return frame


def create_report_dir(path):
    '''Creates a result folder and sets it by default when writing files
        path = r let to the model's sensor'''
    if os.path.exists((path+r'\\reports')):
        os.chdir(path+r'\\reports')
    else:
        os.chdir(path)
        os.mkdir('reports')
        os.chdir(path+r'\\reports')


def lang_convert(df, coll_name):
    """функция меняет символы кириллицы на латиницу
    без осуществления перевода.
    На вход DataFrame и название колонки"""
    df[coll_name] = df[coll_name].apply(lambda x:
                                        slugify(x, lowercase=False)
                                        if isinstance(x, str) else x)


def gtm_effect(name, gtm_date, hist_table, target_period=12):
    """функция выполняет оценку средних показателей до проведения
    мероприятий на скважине и после них
    name - имя скважины
    gtm_date - дата проведения ГТМ в формате datetime
    hist_table - dataframe с историей добычи
    target_period - количество месяцев до и после ГТМ,
        в которое будет проводится сравнение"""

    period = pd.date_range(start=gtm_date-target_period*MonthBegin(),
                           periods=target_period*2, freq='MS')
    wellhist = hist_table[hist_table.well == name]
    df = wellhist[wellhist.date.isin(period)].groupby(
        wellhist.date > gtm_date).mean()
    df['well'] = name
    df['date'] = gtm_date
    df.index.name = 'period'
    df.reset_index(inplace=True)
    df['period'] = df.period.map({False: 'before', True: 'arter'})
    return df


# WARN: функция как таковая ужасно кривая, нужно переписать
def gtm_pivot_table(frame, hist):
    """Функция по созданию единой сводной таблицы эффектов ГТМ"""
    effects = frame.apply(lambda x:
                          gtm_effect(x.well, x.date, hist_table=hist), axis=1)
    effects = pd.concat(effects.to_list())
    res = pd.pivot_table(effects, columns='period', index=['well', 'date'],
                         values=['oil', 'gas', 'water', 'wefac'],
                         aggfunc='mean')
    return res
