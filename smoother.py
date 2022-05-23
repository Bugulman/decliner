#Automaticaly recalculate=false
#Single model=false
from datetime import datetime
import pandas as pd
import datetime
import os
import numpy as np
from scipy import signal
# import transliterate
from oily_report import create_report_dir, model_frame, dataframe_creater, interpolate_press_by_sipy,interpolate_prod_by_sipy


# keyword = {'wells': get_wells_from_filter ('Фильтр по скважинам 1'), 'mod': get_all_models(), 'step': get_all_timesteps()}


def histor_smoothing(df):
	"""Relives and smoothes pressure in source data
	:arg1: TODO
	:kwarg: navigator API keyword = {'grou':get_all_groups(),
									'wells':get_all_wells(),
									'mod': get_all_models(),
									'step':get_all_timesteps()} 
	:returns: pandas DataFrame with smoothing press
	"""
	df['QLIQ'] = df['QOIL']+df['QWAT']
	df['WCT']=(df['QLIQ']-df['QOIL'])/df['QLIQ']
	df['status'] = 'prod'
	df.loc[df['QWIN']>0, 'status'] = 'inj'
	df.loc[((df['QWIN']==0)&(df['QLIQ']==0)), 'status'] = 'not_work'
	df.loc[((df['QWAT']>0)&(df['QOIL']==0)), 'status'] = 'water_prod'
	df['THPH']=df['THPH'].replace([-999,0], np.nan)
	df['BHPH']=df['BHPH'].replace([-999,0], np.nan)
	df.loc[((df['BHPH']>df['THPH'])&(df['status']=='prod')), 'THPH'] = np.NaN
	df=pd.DataFrame(df.groupby(by='well').apply(interpolate_press_by_sipy))
	df.reset_index(drop=True, inplace=True)
	df=pd.DataFrame(df.groupby(by='well').apply(interpolate_prod_by_sipy))
	df.reset_index(drop=True, inplace=True)
	df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
	df['SOIL']=df['SQLIQ']*(1-df['SWCT'])
	df['SPROD']=df['SQLIQ']/(df['STHPH']-df['SBHPH'])
	df['PROD']=df['QLIQ']/(df['THPH']-df['BHPH'])
	df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
	df['SPROD']=df['SQLIQ']/(df['STHPH']-df['SBHPH'])
	df['PROD']=df['QLIQ']/(df['THPH']-df['BHPH'])
	df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
	return df


def main():
    print('lets go')
    create_report_dir(path=get_project_folder())
    frame = histor_smoothing(model_frame, keyword)
    # импорт сглаженных данных в навигатор
    bhp = graph(type='well', default_value=0)
    thp = graph(type='well', default_value=0)
    liq = graph(type='well', default_value=0)
    oil = graph(type='well', default_value=0)
    wct = graph(type='well', default_value=0)
    sprod = graph(type='well', default_value=0)
    prod = graph(type='well', default_value=0)
    mprod = graph(type='well', default_value=0)
    press_diff = graph(type='well', default_value=0)
    for index, rows in frame.iterrows():
        w = get_well_by_name(rows['well'])
        t = get_timestep_from_datetime(
            pd.to_datetime(rows['date']).date(), mode='nearest')
        zab = float(rows['SBHPH'])
        plast = float(rows['STHPH'])
        w_liq = float(rows['SQLIQ'])
        w_oil = float(rows['SOIL'])
        w_wct = float(rows['SWCT'])
        w_sp = float(rows['SPROD'])
        w_p = float(rows['PROD'])
        m_p = float(rows['MPROD'])
        p_diff = float(rows['Pres_dif'])
        bhp[w, t] = zab
        thp[w, t] = plast
        liq[w, t] = w_liq
        oil[w, t] = w_oil
        wct[w, t] = w_wct
        sprod[w, t] = w_sp
        prod[w, t] = w_p
        mprod[w, t] = m_p
        press_diff[w, t] = p_diff
    export(bhp, name='SBHP', units='pressure')
    export(thp, name='STHP', units='pressure')
    export(liq, name='SLIQ', units='liquid_surface_rate')
    export(oil, name='SOIL', units='liquid_surface_rate')
    export(wct, name='SWCT', units='no')
    export(sprod, name='SPROD', units='no')
    export(prod, name='PROD', units='no')
    export(mprod, name='Model_PROD', units='no')
    export(press_diff, name='Pressure diff', units='no')
    #frame['well']=frame['well'].apply(lambda x: transliterate.translit(x, 'ru'))
    frame.to_csv('productiviti.csv')
