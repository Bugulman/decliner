import chardet
import py7zr
import zipfile
import os
import time
from tqdm import tqdm
from pathlib import Path
import re
import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import pprint
import sqlite3
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# %%

# NOTE: подключение к базе sqllite
engine = create_engine('sqlite:///press.db')

# FAQ:часть первая - парсинг единичного файла
# %%


def get_date(html_doc):
    """Функция принимает html документ и вытаскивает все даты"""
    soup = BeautifulSoup(html_doc)
    date = soup.find_all(string=re.compile(r'\d{2}.\d{2}.\d{2,4}'))
    date = date[-1].replace("/", ".")
    try:
        date = datetime.strptime(date, '%d.%m.%Y')
    except:
        date = datetime.strptime(date, '%d.%m.%y')
    return date


def get_well(html_doc):
    """Вытаскивает из документа html название скважины и название куста, к которому
    скважина принадлежит"""
    string = re.compile(
        r'скважины \d{1,2}-\d{1,2}.*участка .{2,9}?\s')
    well_html = string.findall(html_doc)
    # print(well_html)
    well = re.findall(
        r'скважины (\d{1,2}-\d{1,2}).*участка (.{2,9}?)\s', well_html[0])
    return well


def get_well_df(html_file_path):
    """get_well_dfПарсим таблицу с данными по скважинам"""
    df = pd.read_html(html_file_path, skiprows=7)
    df = df[0]
    df = df.iloc[:, :15]
    df.columns = ['time', 'w_ptr', 'w_tust', 'w_pztr', 'w_pzab', 'w_tzab',
                  's_pbefsh', 's_tbefsh', 's_pafsh', 's_tafsh',
                  's_pkust_s', 's_tkust_s', 's_pukpg', 's_tukpg', 'rate']
    df.time = pd.to_numeric(df.time.str.replace(':00', ''))
    df.time = pd.to_timedelta(df.time, unit='h', errors='coerce')
    return df


# %%


def get_encoding(file):
    """docstring for get_encoding"""
    with open(file, 'rb') as f:
        data = f.read(100000)
        result = chardet.detect(data)
        return (result['encoding'])


def parse_well_telemetry(file):
    """docstring for parse_well_telemetry"""
    encod = get_encoding(file)
    with open(file, 'r', encoding=encod) as var:
        html_doc = var.read()
    date = get_date(html_doc)
    well, kust = get_well(html_doc)[0]
    df = get_well_df(file)
    df.time = df.time+date
    df['well'] = well
    df['kust'] = kust
    df['path'] = str(file)
    df['file'] = file.parts[-1]
    return df


# %%
file = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/temp/Kust5-2_20230106.htm')
# file = Path(
# r'/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/temp/Kust1-1_20170603.htm')
encod = get_encoding(file)
with open(file, 'r', encoding=encod) as var:
    html_doc = var.read()
date = get_date(html_doc)
date

df = parse_well_telemetry(file)
df['w_ptr']
# %%
# WARN:часть вторая - нужно найти все файлы для парсинга, а кое какие и распаковать

root_dir = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/Архив данных промысла')
temp_dir = Path(
    r'/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/temp')


# %%
def zip_extract(path, target_path):
    """docstring for zip_extract"""
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
    except:
        with py7zr.SevenZipFile(path, 'r') as z:
            z.extractall(target_path)


def parse_html_file(path):
    with open('telemetry_erorrs.txt', 'w+') as var:
        for file in tqdm(path.glob('**/*.htm*')):
            finder = re.compile('.*')
            if finder.search(str(file)) is not None:
                try:
                    df = parse_well_telemetry(file)
                    df.to_sql('telem_press', con=engine, if_exists='append')
                except:
                    print(file)
                    var.write(str(file)+'\n')
                    continue


# %%
# NOTE: распаковываем архивы
with open('telemetry_erorrs.txt', 'w+') as var:
    for file in root_dir.glob('**/*.zip*'):
        finder = re.compile('.*')
        if finder.search(str(file)) is not None:
            try:
                zip_extract(str(file), str(temp_dir))
                print(file)
            except:
                continue
# %%
# NOTE: обрабатываем htm файлы
parse_html_file(root_dir)
parse_html_file(temp_dir)

# %%

with open('telemetry_erorrs.txt', 'r') as var:
    file = var.readlines()
    print(file)

# %%
zip_extract('/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/Архив данных промысла/2017/Август/А1-1.zip', str(temp_dir))


# Указываем корневую директорию для поиска архивов
text = "<td colspan=15 height=21 class=xl789323 style='height:15.75pt'>Параметры \
  работы скважины 13-4<span style='mso-spacerun:yes'>  </span>участка А-1\
  Уренгойского НГКМ</td>"
text = '''td colspan='2' class='x71' width='131' x:num="44958" x:fmla="=#REF!">01/02/23</td>'''
test = re.compile(r'скважины \d{1,2}-\d{1,2}.*участка .{2,9}?\s')
test = re.compile(r'\d{2}.\d{2}.\d{2,4}')

test.findall(text)

root_dir = Path("/home/albert.vafin/Downloads/Kust1-1_20220301.htm")
root_dir.unlink()
root_dir.exists()
