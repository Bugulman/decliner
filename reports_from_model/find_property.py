#Automaticaly recalculate=true
#Single model=false
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


date = '01.01.2013'
parametr = 'permx'
# Для работы скрипта выгружаем из модели wellpick файлы с параметром по x:y:z и i:j:k
# данные по требуемому параметру с координатами x y
dept_file = 'MD.inc'
# данные по требуемому параметры с координатами i j k
ijk_file = 'ijk.inc'
# данные по зонам вскрытия пластов с координатами i j k для разбивки по пластам
zone_file = 'ZONE_wellpicks_ijk.inc'
zone_dict = {1: 'zone1',
             2: 'zone2'}

olr.create_report_dir(path=get_project_folder())
print(os.getcwd())

# формирование информации из модели

m = get_model_by_name('BLACK_OIL_DEMO')
t = [x for x in get_all_timesteps() if x.name == date]
t = t[0]


with open('for_lost_perf.csv', 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow('well, i, j, k, lpr, lpt, wwir, wwit'.split(','))
    for w in get_all_wells():
        for c in w.connections:
            writer.writerow([str(c.well), c.i, c.j, c.k, float(clpr[m, c, t]), float(
                clpt[m, c, t]), float(cwir[m, c, t]), float(cwit[m, c, t])])

# Загрузка информации из файлов
depth = pd.read_table(dept_file, index_col=None, skiprows=4, sep=' ', names=[
                      'well', 'x', 'y', 'depth', parametr], usecols=[0, 1, 2, 3, 5])
ijk = pd.read_table(ijk_file, index_col=None, skiprows=3, sep=' ', names=[
                    'well', 'i', 'j', 'k', 'del', parametr], usecols=[0, 1, 2, 3, 5])
plast = pd.read_table(zone_file, index_col=None, skiprows=3, sep=' ', names=[
                      'well', 'i', 'j', 'k', 'del', 'zone'], usecols=[0, 1, 2, 3, 5])
profile = pd.read_csv('for_lost_perf.csv')
profile.columns = ['well', 'i', 'j', 'k', 'lpr', 'lpt', 'wwir', 'wwit']
profile.well = profile.well.astype('str')
# предобработка данных
plast['zone'] = plast['zone'].map(zone_dict)

merged_picks = pd.merge(left=depth, right=ijk, left_on=[
                        'well', parametr], right_on=['well', parametr])
merged_picks = pd.merge(left=merged_picks, right=plast, left_on=[
                        'well', 'i', 'j', 'k'], right_on=['well', 'i', 'j', 'k'])
merged_picks['well'] = merged_picks['well'].str.replace("'", "")

merged_picks = pd.merge(left=merged_picks, right=profile, how='left',
                        left_on=['well', 'i', 'j', 'k'], right_on=['well', 'i', 'j', 'k'])
merged_picks.fillna(0, inplace=True)

merged_picks = merged_picks.groupby(['well', 'zone']).agg({'i': 'min', 'j': 'min', 'k': ['min', 'max'], 'lpr': 'sum',
                                                           'lpt': 'sum', 'wwir': 'sum', 'wwit': 'sum',
                                                           'depth': ['min', 'max'], parametr: 'median'})  # .reset_index()
merged_picks = merged_picks.reset_index()
merged_picks.columns = ['well', 'zone', 'i', 'j', 'k', 'k2', 'lpr',
                        'lpt', 'wwir', 'wwit', 'depth', 'depth2', parametr]
merged_picks.to_excel('wells_profile.xlsx')
