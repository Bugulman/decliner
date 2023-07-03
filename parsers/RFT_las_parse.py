import lasio as ls
import py7zr
import zipfile
import rarfile
import time
from tqdm import tqdm
from pathlib import Path
import re
import pandas as pd
from sqlalchemy import create_engine
import pprint
import sqlite3
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# %%

# NOTE: подключение к базе sqllite
engine = create_engine('sqlite:///press.db')

# %%
# WARN:Прописываем пути где хотим распаковать все архивы

root_dir = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/ПГИ')
temp_dir = root_dir.joinpath('unzipped_files')
# %%


def unzip_file(path, target_path):
    with zipfile.ZipFile(path, 'r') as zip_file:
        zip_file.extractall(target_path)


def unrar_file(path, target_path):
    with rarfile.RarFile(path, 'r') as rar_file:
        rar_file.extractall(target_path)


def un7z_file(path, target_path):
    with py7zr.SevenZipFile(path, 'r') as z:
        z.extractall(target_path)


# %% NOTE: распаковываем архивы
with open('RFT_erorrs.txt', 'w+') as var:
    for file in root_dir.glob('**/*.zip*'):
        try:
            unzip_file(str(file), str(temp_dir))
        except:
            var.write(str(file)+'\n')
            print(file)
            continue
    for file in root_dir.glob('**/*.rar*'):
        try:
            unrar_file(str(file), str(temp_dir))
        except:
            var.write(str(file)+'\n')
            print(file)
            continue
    for file in root_dir.glob('**/*.7z*'):
        try:
            un7z_file(str(file), str(temp_dir))
        except:
            var.write(str(file)+'\n')
            print(file)
            continue
# %%


def get_metadata(las_file):
    """docstring for get_metadata"""
    wellname = las_file.sections['Well']['WELL'].value
    logdate = las_file.sections['Well']['DATE'].value
    try:
        logdate = get_date(logdate)
    except:
        print(f'Не удалось преобразовать дату {logdate}')
    return wellname, logdate


def get_date(string_with_date, regex=r'\d{1,2}\.\d{2}\.\d{2,4}'):
    """Функция принимает строку и вытаскивает все даты"""
    re_date = re.compile(regex)
    date = re_date.findall(string_with_date)
    date = date[-1].replace("/", ".")
    try:
        date = datetime.strptime(date, '%d.%m.%Y') if len(
            date) > 8 else datetime.strptime(date, '%d.%m.%y')
    except:
        print(f'Не удалось преобразовать дату {date}')
    return date


def get_curves(las_file, regex=r'.*[Mm]anom[a-z]*|.*[Dd]ebit[a-z]*|.*[Rr]ashod[a-z]*|.*[Ss]hum[a-z]*|.*[Tt]ermo'):
    """docstring for get_curves"""
    aim = re.compile(regex)
    tar_curves = [curve.descr.lower() for curve in las_file.curves
                  if aim.search(curve.descr.lower()) != None]
    return tar_curves


def rft_las_parse(file):
    """Функция переводит RFT исследования из формата las в df"""
    las = ls.read(file)
    df = las.df()
    curves = get_curves(las)
    # print(las.curves)
    mnem_names = [
        curve.mnemonic for curve in las.curves if curve.descr.lower() in curves]
    curve_names = {
        curve.mnemonic: curve.descr.lower() for curve in las.curves}
    # print(curve_names)
    df = df.loc[:, mnem_names]
    df.rename(columns=curve_names, inplace=True)
    for cols in df.columns:
        dif_name = cols+'_diff'
        df[dif_name] = df[cols].diff()
    wellname, logdate = get_metadata(las)
    df = df.stack().reset_index()
    df.insert(0, 'Well', wellname)
    df.insert(1, 'Date', logdate)
    return df.reset_index()


# %% NOTE: обрабатываем ласы
with open('RFT_erorrs.txt', 'w+') as var:
    # FAQ: не забудь, что есть еще и LAS
    for file in root_dir.glob('**/*.LAS*'):
        try:
            df = rft_las_parse(file)
            df['Path'] = str(file)
            # las = ls.read(file)
            # well, date = get_metadata(las)
            # name = f'Well_{well}_{date}.csv'
            # df.columns = ['dept', 'well', 'date',
            # 'manom', 'diff_manom', 'path']
            # df.to_csv(root_dir.joinpath('RFT', name))
            df.to_sql('rft', con=engine, if_exists='append')
        except:
            var.write(str(file)+'\n')
            print(file)
            continue
    for file in root_dir.glob('**/*.las*'):
        try:
            df = rft_las_parse(file)
            df['Path'] = str(file)
            # las = ls.read(file)
            # well, date = get_metadata(las)
            # name = f'Well_{well}_{date}.csv'
            # df.columns = ['dept', 'well', 'date',
            # 'manom', 'diff_manom', 'path']
            # df.to_csv(root_dir.joinpath('RFT', name))
            df.to_sql('rft', con=engine, if_exists='append')
        except:
            var.write(str(file)+'\n')
            print(file)
            continue


# %% BUG: отладки и мусор
las = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/ПГИ/9 куст/А 9-5/21.06.2018/las/A9-5_Ureng_pgi_21-23.06.2018_statika.las')

las = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/ПГИ/unzipped_files/15.09.2013/LAS/A4-3_STAT.LAS'
)

las_file = ls.read(las)
las_file.sections.keys()  # ['Other information']
get_curves(las_file)
las_file.sections['Other']  # ['Other information']

fr = rft_las_parse(las)
fr.level_1.unique()
fr.columns
fr.DEPT = fr.DEPT.astype('str')
fr.info()
fr.to_sql('rft', con=engine, if_exists='append')
fr.unstack().reset_index()
well, date = get_metadata(las_file)
name = f'Well_{well}_{date}.csv'
fr.to_sql('rft', con=engine, if_exists='append')

df.to_csv(root_dir.joinpath('RFT', name))
