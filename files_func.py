import pandas as pd
import numpy as np
import os
import urllib
import datetime
import matplotlib.pyplot as plt

f = {'Горизонт': ['mean'],
     'Кол-во часов экспл всего по доб. скваж': ['max'],
     'Добыча нефти за мес по скваж, т': ['sum'],
     'Добыча воды за мес по скваж, т': ['sum'],
     'Добыча воды за мес по скважине, м3': ['sum'],
     'Кол-во часов работы всего по нагн. скваж': ['max'],
     'Общая закачка всего по скваж за мес, м3': ['sum']}
d = {'Горизонт': ['mean'],
     'P заб ВНК': ['mean'],
     'P пласт ВНК': ['mean']}


def hist_table_prepare(frames, gor_num):
    """функция для подготовки данных из лисички в данные для обработки скриптами"""
    prod_df, press_df = frames
    prod_df['Горизонт'] = prod_df['Горизонт'].astype('int')
    press_df['Горизонт'] = press_df['Код гориз'].astype('int')
    prod_df = prod_df.loc[prod_df['Горизонт'].isin(gor_num)]
    prod_df = prod_df.loc[prod_df['Горизонт'].isin(gor_num)]
    press_df['P заб ВНК'] = pd.to_numeric(
        press_df['P заб ВНК'], errors='coerce')
    press_df['P пласт ВНК'] = pd.to_numeric(
        press_df['P пласт ВНК'], errors='coerce')
    prod_df = pd.DataFrame(prod_df.groupby(['№ скваж', 'Дата'])['Горизонт', 'Кол-во часов экспл всего по доб. скваж',
                                                                           'Добыча нефти за мес по скваж, т', 'Добыча воды за мес по скваж, т',
                                                                           'Добыча воды за мес по скважине, м3',
                                                                           'Кол-во часов работы всего по нагн. скваж',
                                                                           'Общая закачка всего по скваж за мес, м3'].agg(f))
    prod_df = prod_df.reset_index()
    press_df = pd.DataFrame(press_df.groupby(['№ скваж', 'Дата'])[
                            'Горизонт', 'P заб ВНК', 'P пласт ВНК'].agg(d))
    press_df = press_df.reset_index()
    df = pd.merge(prod_df, press_df, on=[
                  '№ скваж', 'Дата'], how='left')
    df.columns = ['№ скваж', 'Дата', 'Горизонт_x', 'Кол-во часов экспл всего по доб. скваж',
                  'Добыча нефти за мес по скваж, т', 'Добыча воды за мес по скваж, т', 'Добыча воды за мес по скважине, м3',
                  'Кол-во часов работы всего по нагн. скваж', 'Общая закачка всего по скваж за мес, м3', 'Горизонт_y',
                  'BHPH', 'THPH']
    df['QOIL'] = df['Добыча нефти за мес по скваж, т'] / \
        (df['Кол-во часов экспл всего по доб. скваж'])*24
    df['QWAT'] = df['Добыча воды за мес по скваж, т'] / \
        (df['Кол-во часов экспл всего по доб. скваж'])*24
    df['QWIN'] = df['Общая закачка всего по скваж за мес, м3'] / \
        (df['Кол-во часов работы всего по нагн. скваж'])*24
    df['QLIQ'] = df['QOIL']+df['QWAT']
    df['well'] = df['№ скваж']
    df['date'] = df['Дата']
    df.set_index(['date'], inplace=True)
    df['date'] = df['Дата']
    return df