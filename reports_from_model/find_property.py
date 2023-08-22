# Automaticaly recalculate=false
# Single model=false
# пишите здесь ваш код
# пишите здесь ваш код
# пишите здесь ваш код
import oily_report as olr
import os
import time
import csv
import pandas as pd
start_time = time.time()
# Для работы скрипта выгружаем из модели wellpick файлы с насыщением по x:y:z и i:j:k и файл с соответсвующими зонами пласта FIPNUM
# ВАЖНО!!! в fipnum должны быть индексы по пластам! если нет, то работа скрипта будет не корректной
# данные по насыщению с координатами x y
dept_file = 'Насыщенность нефтью_wellpics_MD.inc'
# данные по насыщению с координатами i j k
ijk_file = 'Насыщенность нефтью_wellpics_ijk.inc'
# данные по зонам вскрытия пластов с координатами i j k
zone_file = 'ZONE_wellpics_ijk.inc'
zone_dict = {1: 'zone1',
             2: 'zone2'}

olr.create_report_dir(path=get_project_folder())
print(os.getcwd())

# формирование информации из модели

m = get_model_by_name('')
t = [x for x in get_all_timesteps() if x.name == '01.01.2023']


with open('for_lost_perf.csv', 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow('well, i, j, k, lpr, lpt, wwir, wwit'.split(','))
    for w in get_all_wells():
        if wlpth[m, w].max(dates='all') > 0 or wwith[m, w].max(dates='all') > 0:
            for c in w.connections:
                writer.writerow([c.well, c.i, c.j, c.k, float(clpr[m, c, t]),
                                 float(clpt[m, c, t]), float(cwir[m, c, t]), float(cwit[m, c, t])])

# Загрузка информации из файлов
depth = pd.read_table(dept_file, index_col=None, skiprows=4, sep=' ', names=[
                      'well', 'x', 'y', 'depth', 'soil'], usecols=[0, 1, 2, 3, 5])
ijk = pd.read_table(ijk_file, index_col=None, skiprows=3, sep=' ', names=[
                    'well', 'i', 'j', 'k', 'del', 'soil'], usecols=[0, 1, 2, 3, 5])
plast = pd.read_table(zone_file, index_col=None, skiprows=3, sep=' ', names=[
                      'well', 'i', 'j', 'k', 'del', 'zone'], usecols=[0, 1, 2, 3, 5])
profile = pd.read_csv('for_lost_perf.csv')
profile.columns = ['well', 'i', 'j', 'k', 'lpr', 'lpt', 'wwir', 'wwit']
# предобработка данных
plast['zone'] = plast['zone'].map(zone_dict)

merged_picks = pd.merge(left=depth, right=ijk, left_on=[
                        'well', 'soil'], right_on=['well', 'soil'])
merged_picks = pd.merge(left=merged_picks, right=plast, left_on=[
                        'well', 'i', 'j', 'k'], right_on=['well', 'i', 'j', 'k'])
merged_picks['well'] = merged_picks['well'].str.replace("'", "")
merged_picks = pd.merge(left=merged_picks, right=profile, how='left',
                        left_on=['well', 'i', 'j', 'k'], right_on=['well', 'i', 'j', 'k'])
merged_picks.fillna(0, inplace=True)

summ = pd.merge(merged_picks.reset_index(), zapas_frame.reset_index(), on=[
                'well', 'zone'], how='left')
summ = summ.groupby(['well', 'zone']).agg({'i': 'min', 'j': 'min', 'k': ['min', 'max'], 'lpr': 'sum',
                                                            'lpt': 'sum', 'wwir': 'sum', 'wwit': 'sum', 0: 'mean',
                                          'depth': ['min', 'max'], 'soil': 'median'})  # .reset_index()
summ = summ.reset_index()
summ.columns = ['well', 'zone', 'i', 'j', 'k', 'k2', 'lpr',
                'lpt', 'wwir', 'wwit', 0, 'depth', 'depth2', 'soil']
summ.to_excel('for_perf.xlsx')
