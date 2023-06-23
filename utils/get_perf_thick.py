#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/23
# @Author  : <VAR>
# @File    : get_perf_thick.py
# @Description:


import pandas as pd
import os

date = '01.01.2013'
parametr = 'permx'
m = get_model_by_name('BLACK_OIL_DEMO')
# Для работы скрипта выгружаем из модели wellpick файлы с параметром по x:y:z и i:j:k
# данные по требуемому параметру с координатами x y
dept_file = 'MD.inc'
# данные по требуемому параметры с координатами i j k
ijk_file = 'ijk.inc'
# данные по зонам вскрытия пластов с координатами i j k для разбивки по пластам


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
                      'well', 'x', 'y', 'depth', parametr], usecols=[0, 1, 2, 3, 5])
ijk = pd.read_table(ijk_file, index_col=None, skiprows=3, sep=' ', names=[
                    'well', 'i', 'j', 'k', 'del', parametr], usecols=[0, 1, 2, 3, 5])


# формирование информации из модели

t = [x for x in get_all_timesteps() if x.name == date]
t = t[0]

model_frame = []
for t in get_all_timesteps():
    for w in get_all_wells():
        for c in w.connections:
            model_frame.append([str(c.well), t.name, c.i, c.j, c.k, float(clpr[m, c, t]), float(cwir[m, c, t]))])

model_frame=pd.DataFrame(model_frame)

model_frame.columns=['well', 'i', 'j', 'k', 'lpr', 'lpt', 'wwir', 'wwit']
model_frame.well=model_frame.well.astype('str')

# предобработка данных
merged_picks=pd.merge(left = depth, right = ijk, left_on = [
                        'well', parametr], right_on = ['well', parametr])
merged_picks['well']=merged_picks['well'].str.replace("'", "")


# merged_picks=pd.merge(left = merged_picks, right = model_frame, how = 'left',
#                         left_on = ['well', 'i', 'j', 'k'], right_on = ['well', 'i', 'j', 'k'])
#
# merged_picks.fillna(0, inplace = True)
#
# merged_picks=merged_picks.groupby(['well', 'zone']).agg({'i': 'min', 'j': 'min', 'k': ['min', 'max'], 'lpr': 'sum',
#                                                            'lpt': 'sum', 'wwir': 'sum', 'wwit': 'sum',
#                                                            'depth': ['min', 'max'], parametr: 'median'})  # .reset_index()
# merged_picks=merged_picks.reset_index()
# merged_picks.columns=['well', 'zone', 'i', 'j', 'k', 'k2', 'lpr',
#                         'lpt', 'wwir', 'wwit', 'depth', 'depth2', parametr]
# merged_picks.to_excel('wells_profile.xlsx')
