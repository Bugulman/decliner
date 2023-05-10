import os
import time
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
p = Path.cwd()
p
# con = sqlite3.connect(p.joinpath('pasport.db'))

# con.close()
# %%
# NOTE:подключение к базе Postgresql
engine = create_engine(
    'postgresql://test:test@localhost:5434/ungkm')
# %%

# NOTE: подключение к базе sqllite
engine = create_engine('sqlite:///press.db')

# %%
file = Path(r'/cluster3/public/2023/UNGKM/Data Achimgas/Телеметрия/Архив данных промысла/2008/07.2008/11.07.2008/K31_11.htm')

# FAQ:часть первая - парсинг единичного файла
# %%


def get_date(html_doc):
    """Функция принимает html документ и вытаскивает все даты"""
    soup = BeautifulSoup(html_doc)
    date = soup.find_all(string=re.compile(r'\d{2}.\d{2}.\d{4}'))
    date = datetime.strptime(date[0], '%d.%m.%Y')
    return date


def get_well(html_doc):
    """Вытаскивает из документа html название скважины и название куста, к которому
    скважина принадлежит"""
    soup = BeautifulSoup(html_doc)
    well_html = soup.find_all(string=re.compile(
        r'скважины .{2,5}? участка.{2,5}? '))
    well = re.findall(
        r'скважины (.{2,5}?) участка(.{2,5}?) ', well_html[0])
    return well


def get_well_df(html_file_path):
    """get_well_dfПарсим таблицу с данными по скважинам"""
    df = pd.read_html(file, skiprows=7)
    df = df[0]
    df.columns = ['time', 'w_ptr', 'w_tust', 'w_pztr', 'w_pzab', 'w_tzab',
                  's_pbefsh', 's_tbefsh', 's_pafsh', 's_tafsh',
                  's_pkust_s', 's_tkust_s', 's_pukpg', 's_tukpg', 'rate', 'position']
    df.time = pd.to_numeric(df.time.str.replace(':00', ''))
    df.time = pd.to_timedelta(df.time, unit='h', errors='coerce')
    return df
    pd.to_timedelta(1, unit='h')

# %%


def parse_well_telemetry(file):
    """docstring for parse_well_telemetry"""
    with open(file, 'r', encoding='cp1251') as var:
        html_doc = var.read()
    date = get_date(html_doc)
    well, kust = get_well(html_doc)[0]
    df = get_well_df(file)
    df.time = df.time+date
    df['well'] = well
    df['kust'] = kust
    return df


# %%
# WARN:
df = parse_well_telemetry(file)


# %%
