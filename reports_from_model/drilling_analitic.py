# %
import pandas as pd
import datetime as dt
import calendar
import numpy as np
from pathlib import Path

# %%
file = Path('/cluster3/home/albert.vafin/UNGKM/Designer/reports/press_prod.csv')

df = pd.read_csv(file, parse_dates=['date'])

df['day_in_month'] = df['date'].apply(lambda x: calendar.monthrange(x.year, x.month)[1])
df['work_day'] = df['day_in_month']*df['wefac']

df['oil_prod']=df['oil']*df['day_in_month']*df['wefac']
df['wat_prod']=df['water']*df['day_in_month']*df['wefac']
df['liq_prod']=df['oil_prod']+df['wat_prod']
df['gas_prod']=df['gas']*df['day_in_month']*df['wefac']
df['wct']=df['wat_prod']/df['liq_prod']*100
# %%
def drill_year (df):
    df['Year']=df['date'].dt.year
    df['Start_date'] = df['date'].min()
    df['Start_year'] = df['Year'].min()
    return df


# %%
def work_day (df):
    df['Day'] = df['date']-df['date'].min()
    return df

# %%

def work_month (df):
    df['Month'] = np.linspace(1, len(df), len(df))
    return df

# %%
def first_deb (df, x=3):
    df['qo'] = df['oil_prod'].head(x).sum()/df['work_day'].head(x).sum()*24
    df['ql'] = df['liq_prod'].head(x).sum()/df['work_day'].head(x).sum()*24
    df['qg'] = df['gas_prod'].head(x).sum()/df['work_day'].head(x).sum()*24
    return df

# %%
def cummulitive (df):
    df['tot_oil'] = df['oil_prod'].cumsum()
    df['tot_liq'] = df['liq_prod'].cumsum()
    df['tot_gas'] = df['gas_prod'].cumsum()
    return df

# %%
def Kpad (df):
    df['kpad'] = df['oil']/df['oil'].shift(1)
    return df
# %%
df.reset_index(drop=True, inplace = True) 
functions = [drill_year, work_month, work_day, first_deb, cummulitive, Kpad]
for f in functions:
    df=pd.DataFrame(df.groupby(by='well').apply(f))
    df.reset_index(drop=True, inplace = True) 
# %%

drilling_pivot = df.groupby('well').agg({'qo':'mean', 'ql':'mean', 'Start_year':'mean'})
drilling_pivot
