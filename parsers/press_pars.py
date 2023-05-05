# %%
import os
import time
from pathlib import Path
import re
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import numpy as np
import pprint
import sqlite3
import csv
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

# Перечень файлов паспортов скважин
# WARN: запускается единожды!
p = Path(r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений')
print(p)

with open('press.txt', 'w+') as var:
    for file in p.glob('**/*.CSV*'):
        finder = re.compile('GA.*')
        if finder.search(str(file)) != None:
            try:
                var.write(str(file)+'\n')
                print(file)
            except:
                continue
# %%

text = r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений/2014/забойники от 29.07.14/18 куст/JUL14/GA140701.CSV'

text = r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений/2022/КВД скв. №А4-3/GA220818.CSV'
# %%

# FAQ:обработка даты
p = Path(text)
str(p)


def get_date_from_filename(path):
    """функция принимает путь к файлу и формирует дату из названия файла
    в формате yymmdd"""
    date = re.findall('\d{6}', path.parts[-1])
    date = datetime.strptime(date[0], '%y%m%d')
    return date

# %%
# FAQ:обработка единичного csv файла


def get_wells(file_path: str):
    """функция читает заголовок csv файла и заирает оттуда информация по 
    имеющимся в файле скважинам"""
    header = []
    with open(file_path, 'r', encoding='cp1251') as var:
        line = csv.reader(var)
        for row in line:
            if len(row) <= 2:
                header.append(row[0].strip())
            else:
                break
    return header


def main(file_path: Path):
    header = get_wells(str(file_path))
    date = get_date_from_filename(file_path)
    full_frame = pd.read_csv(file_path, skiprows=len(
        header)+2, engine='python', encoding='cp1251')
    # print(header)
    for seq in range(len(header)):
        print(header[seq])
        subframe = full_frame.iloc[:, [0, 2*seq+1, 2*seq+2]]
        # print(subframe.head())
        subframe.columns = ['time', 'press', 'temp']
        # print(subframe.head())
        subframe.time = pd.to_timedelta(subframe.time, errors='coerce')
        subframe = subframe[~subframe.time.isnull()]
        subframe.time = subframe.time+date
        # print(subframe)
        subframe.index = subframe.time
        subframe.press = pd.to_numeric(subframe.press)
        subframe.temp = pd.to_numeric(subframe.temp)
        subframe.to_csv('testt.csv')
        subframe = subframe[['press', 'temp']].resample('H').mean()
        subframe['well'] = header[seq]
        subframe['path'] = str(file_path)
        subframe.to_sql('press', con=engine, if_exists='append')

        # print(subframe)
        # else:
        # print(row[0], row[1], row[2])
    # subframe.info()
# %%
text = r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений/2014/забойники от 29.07.14/20 куст/JUL14/GA140720.CSV'

text = r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений/2014/забойники от 29.07.14/20 куст/JUN14/GA140602.CSV'
p = Path(text)
main(p)

header = get_wells(str(p))
date = get_date_from_filename(p)
full_frame = pd.read_csv(p, skiprows=len(
    header)+2, engine='python', encoding='cp1251')

full_frame

full_frame = full_frame.iloc[:, [0, 1, 2]]

full_frame.columns = ['time', 'press', 'temp']

full_frame.time = pd.to_timedelta(full_frame.time, errors='coerce')
full_frame.iloc[115]
full_frame = full_frame[~full_frame.time.isnull()]
full_frame.press = pd.to_numeric(full_frame.press)
full_frame.temp = pd.to_numeric(full_frame.temp)
full_frame.index = full_frame.time
full_frame[['press', 'temp']].resample('H').mean()

full_frame[~full_frame.time.isnull()].to_csv('test.csv')
main(p)
# temp.index = temp.time
# temp[['press', 'temp']].resample('H').mean()
# temp.info()

# %%
# WARN: запускается единожды!
p = Path(r'/cluster3/public/2023/UNGKM/Data Achimgas/Замеры забойных давлений')
# print(p)

with open('press.txt', 'w+') as var:
    for file in p.glob('**/*.CSV*'):
        finder = re.compile('GA.*')
        if finder.search(str(file)) != None:
            try:
                main(file)
                # print(file)
            except:
                print(f'NOT LOADED {file}')
                var.write(str(file)+'\n')
                continue

# %%
# FAQ:отработка регулярок
kust_re = re.compile('/.{0,8}[Кк]уст.{0,8}/')
well_re = re.compile('/.{0,8}[Сс]кв.{0,12}/')
pprint.pprint(finder.findall(text))

text
pd.read_csv(text, skiprows=3, engine='python',
            encoding='cp1251', names=['time', 'press', 'temp'])
