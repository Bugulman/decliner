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
# сводный файл с информацией по запасам
zapas_file = r'D:\project\Minnib_project\SCHED_PATTERNS\scripts\запасы_3\сводная таблица запасов (1).xlsx'
zone = ['well', 'voronon', 'D0', 'D1a', 'D1b1', 'D1b2', 'D1b3', 'argil', 'D1v', 'D1g1', 'D1g2+3', 'D1d', 'mul_gl',
        'mul_bot', 'all']  # шапка для назнавания пластов в файле с запасами
zone_dict = {1: 'D0',
             2: 'kin_gl',
             3: 'VIZV',
             4: 'D1a',
             5: 'D1b1',
             6: 'D1b2',
             7: 'D1b3',
             8: 'argil',
             9: 'D1v',
             10: 'D1g1',
             11: 'D1g2+3',
             12: 'D1d',
             13: 'mul_gl',
             14: 'mul_bot',
             15: 'buf'}

olr.create_report_dir(path=get_project_folder())
print(os.getcwd())

# формирование информации из модели


def max_time():
    for t in get_all_timesteps():
        a = t
    return a


with open('for_lost_perf.csv', 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow('well, i, j, k, lpr, lpt, wwir, wwit'.split(','))
    for m in get_all_models():
        if flpth[m].max(dates='all') > 0:
            for w in get_all_wells():
                if wlpth[m, w].max(dates='all') > 0 or wwith[m, w].max(dates='all') > 0:
                    for c in w.connections:
                        writer.writerow([c.well, c.i, c.j, c.k, float(clpr[m, c, max_time()]), float(
                            clpt[m, c, max_time()]), float(cwir[m, c, max_time()]), float(cwit[m, c, max_time()])])

# Загрузка информации из файлов
depth = pd.read_table(dept_file, index_col=None, skiprows=4, sep=' ', names=[
                      'well', 'x', 'y', 'depth', 'soil'], usecols=[0, 1, 2, 3, 5])
ijk = pd.read_table(ijk_file, index_col=None, skiprows=3, sep=' ', names=[
                    'well', 'i', 'j', 'k', 'del', 'soil'], usecols=[0, 1, 2, 3, 5])
plast = pd.read_table(zone_file, index_col=None, skiprows=3, sep=' ', names=[
                      'well', 'i', 'j', 'k', 'del', 'zone'], usecols=[0, 1, 2, 3, 5])
profile = pd.read_csv('for_lost_perf.csv')
profile.columns = ['well', 'i', 'j', 'k', 'lpr', 'lpt', 'wwir', 'wwit']
zapas_frame = pd.read_excel(zapas_file)
zapas_frame.columns = zone
zapas_frame.index = zapas_frame['well']
zapas_frame.drop(columns='well', inplace=True)
zapas_frame = pd.DataFrame(zapas_frame.stack())
zapas_frame.index.names = ['well', 'zone']  # .reset_index()
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
