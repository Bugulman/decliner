#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/23
# @Author  : <VAR>
# @File    : get_perf_thick.py
# @Description: специально для Азамата
# Для работы скрипта выгружаем из модели wellpick файлы с параметром по x:y:z и i:j:k
# WARN: для корректной работы нужно выгрузить оба файла со сходими настройками
# Объект:траектория Экспорт значения:значение вдоль скважины
# и положить в папку reports в основной папке проекта
# файлы называет "MD.inc" и "ijk.inc"


import pandas as pd
import os
import numpy as np

m = get_model_by_name('SARAI')

dept_file = 'MD.inc'
ijk_file = 'ijk.inc'


def create_report_dir(path):
    '''Creates a result folder and sets it by default when writing files
        path = r let to the model's sensor'''
    if os.path.exists((path+r'\\reports')):
        os.chdir(path+r'\\reports')
    else:
        os.chdir(path)
        os.mkdir('reports')
        os.chdir(path+r'\\reports')


create_report_dir(path=get_project_folder())
print(os.getcwd())

# Загрузка информации из файлов
depth = pd.read_table(dept_file, index_col=None, skiprows=4, sep=' ', names=[
                      'well', 'depth'], usecols=[0, 3])
ijk = pd.read_table(ijk_file, index_col=None, skiprows=4, sep=' ', names=[
                    'well', 'i', 'j', 'k'], usecols=[0, 1, 2, 3])


# формирование информации из модели

model_frame = []
for t in get_all_timesteps():
    for w in get_all_wells():
        for c in w.connections:
            if bool(c.is_opened()[t]):
                # print([str(c.well), t.name,bool(c.is_opened( )[t]), c.i, c.j, c.k, float(clpr[m, c, t]), float(cwir[m, c, t])])
                model_frame.append([str(c.well), t.name, c.i, c.j, c.k, float(
                    clpr[m, c, t]), float(cwir[m, c, t])])

model_frame = pd.DataFrame(model_frame)
model_frame.columns = ['well', 'date', 'i', 'j', 'k', 'lpr', 'wwir']
model_frame.well = model_frame.well.astype('str')
#
# # предобработка данных
df_thick = pd.concat([ijk, depth.depth], axis=1)
df_thick['well'] = df_thick['well'].str.replace("'", "")
df_thick['thick'] = df_thick.depth.diff()
df_thick['thick'] = df_thick['thick'].median()
df_thick = pd.merge(left=model_frame, right=df_thick, how='left',
                    left_on=['well', 'i', 'j', 'k'], right_on=['well', 'i', 'j', 'k'])
#
# Агрегируем финальный датафрейм
# merged_picks = merged_picks.groupby(['well', 'date']).agg({'k': ['min', 'max'], 'lpr': 'sum',
# 'wwir': 'sum', 'depth': ['min', 'max'], 'thick': 'sum'})  # .reset_index()
df_thick = df_thick.groupby(['well', 'date']).agg(
    {'thick': 'sum'})
df_thick = df_thick.reset_index()

df_thick.to_csv('perf_thickness.csv')
