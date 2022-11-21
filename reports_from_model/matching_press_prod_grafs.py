#Automaticaly recalculate=true
#Single model=false
#пишите здесь ваш код
#пишите здесь ваш код
#пишите здесь ваш код
from datetime import datetime
import oily_report as olr
import pandas as pd
import datetime
import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.dates as mdate



locator = mdate.YearLocator()

def q1(x):
    return x.quantile(0.25)

def q2(x):
    return x.quantile(0.75)

def press_graph(y):
    '''Create pic for field/
        y = dataframe from field'''
    
    fig = plt.figure(figsize=(25, 10)) 
    ax1 = plt.subplot()
    ax1.plot(y['STHPH', 'median'], color='k')
    ax1.plot(y['MPRES', 'median'], color='r')
    ax1.fill_between(y.index, y['STHPH', 'q2'], y['STHPH', 'median'],\
                                where=y['STHPH', 'q2']>y['STHPH', 'median'], \
                                facecolor='green', alpha=0.3)
    ax1.fill_between(y.index, y['STHPH', 'q1'], y['STHPH', 'median'],\
                                where=y['STHPH', 'median']>y['STHPH', 'q1'], \
                                facecolor='green', alpha=0.3)
    ax1.fill_between(y.index, y['MPRES', 'q2'], y['MPRES', 'median'],\
                                where=y['MPRES', 'q2']>y['MPRES', 'median'], \
                                facecolor='red', alpha=0.3)
    ax1.fill_between(y.index, y['MPRES', 'q1'], y['MPRES', 'median'],\
                                where=y['MPRES', 'median']>y['MPRES', 'q1'], \
                                facecolor='red', alpha=0.3)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y'))
    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('Press', fontsize=14)
    ax1.grid(False)
    fig.autofmt_xdate()
    fig.savefig(f'graf_press.png')
    
def prod_graph(y):
    '''Create pic for field/
        y = dataframe from field'''
    
    fig = plt.figure(figsize=(25, 10)) 
    ax1 = plt.subplot()
    ax1.plot(y['SPROD', 'median'], color='k')
    ax1.plot(y['MPROD', 'median'], color='r')
    ax1.fill_between(y.index, y['SPROD', 'q2'], y['SPROD', 'median'],\
                                where=y['SPROD', 'q2']>y['SPROD', 'median'], \
                                facecolor='green', alpha=0.3)
    ax1.fill_between(y.index, y['SPROD', 'q1'], y['SPROD', 'median'],\
                                where=y['SPROD', 'median']>y['SPROD', 'q1'], \
                                facecolor='green', alpha=0.3)
    ax1.fill_between(y.index, y['MPROD', 'q2'], y['MPROD', 'median'],\
                                where=y['MPROD', 'q2']>y['MPROD', 'median'], \
                                facecolor='red', alpha=0.3)
    ax1.fill_between(y.index, y['MPROD', 'q1'], y['MPROD', 'median'],\
                                where=y['MPROD', 'median']>y['MPROD', 'q1'], \
                                facecolor='red', alpha=0.3)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y'))
    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('Press', fontsize=14)
    ax1.set_ylim((0,1))
    ax1.grid(False)
    fig.autofmt_xdate()
    fig.savefig(f'graf_prod.png')
    
model=pd.read_csv('productiviti.csv', index_col='date')
model.index =pd.to_datetime(model.index)
model.loc[model['SPROD']<-1, 'SPROD']=np.nan

press_graph(model.loc[model['status']=='prod',['STHPH', 'MPRES']].groupby(model.loc[model['status']=='prod'].index)\
.agg([np.median,q1, q2]))

prod_graph(model.loc[model['status']=='prod',['SPROD', 'MPROD']].groupby(model.loc[model['status']=='prod'].index)\
.agg([np.median,q1, q2]))
