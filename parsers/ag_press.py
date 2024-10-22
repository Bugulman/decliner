#!/usr/bin/env python3
# %%
from pathlib import Path
import re
import pandas as pd
import xlwings as xw
from sqlalchemy import create_engine
from tqdm import tqdm
import numpy as np
from collections import Counter
from pprint import pprint
import os
# %%
os.chdir(r'D:\work\python\decliner\parsers')
    
file = r'c:\Users\reg16\Downloads\AD_press.xlsx'
engine = create_engine('sqlite:///press.db')
# %%
book = xw.Book(file)
sheet = book.sheets['ДАННЫЕ']
# %%
begins = []


for coll in range(0,2298):
    sheet[3, coll].value
    if sheet[3, coll].value==None:
        sheet[3, coll].value='пусто'
    else: 
        pass
        
# %%        
for coll in range(0,2298):
    sheet[3, coll].value
    if sheet[3, coll].value=='%  откр.':
        begins.append(coll) 
    else: 
        pass
# %%
time = sheet.range('B6:B1101').value

# %%
c=Counter(sheet.range((4,1),(4, 2300)).value)

wells = [x for x in sheet.range((1,1),(1, 2300)).value\
    if x != None]
wells = list(zip(wells[2:], begins))
# %%
for well, num in wells:
    print(well, num)
    df = get_records(well, num)
    df.to_sql('ag_press', con=engine, if_exists='append')
    # print(df.shape)

# %%


def get_records(well_name, num):
    # num = 2
    table = sheet.range((6,num),(1102, num+13))
    coll_names = sheet.range((4,num+1),(4, num+13))
    table
    df = table.options(pd.DataFrame).value
    df.index = time
    df.columns = coll_names.value
    df['%  откр.'].ffill(inplace=True)
    # df.info()
    df['well'] = well_name   
    # df = df[[x for x in coll_names.value if x !='пусто']]
    df = df[['well','%  откр.', 'Р уст, МПа', 'Р зт, МПа', \
    'Qсеп. тыс.м3',  'Р зб. МПа', 'Р ГС2, МПа']]
    return df.loc[df['%  откр.'].notnull()]


#%%
well, num = wells[5]
df = get_records(well, num)
df.to_sql('ag_press', con=engine, if_exists='replace')
df.columns
#%%
coll_names = sheet.range((4,num+1),(4, num+13))
coll_names
df[[x for x in coll_names.value if x !='пусто']]
