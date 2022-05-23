import pandas as pd
import pprint
import os
import datetime
import getpass
import urllib
import numpy as np
# import sqlalchemy
from scipy import signal

def dataframe_creater(*args, start='01.01.1950', **kwarg):
    """создает pandas Dataframe с данными из модели.
         Принимает неограниченное количество параметров для
          импорта, позволяет осуществлять импорт как по скважинам 
          так и по группам заданием kwarg
         function for converting navigation format to pandas dataframe
         *args - list of arguments to issue in the frame
             dimens - well, here is one of two:
                        well - for issuing a frame for wells
                        group - for issuing by group"""
    indicators = [x for x in args]
    name = ['Parametr{}'.format(x) for x in range(0, len(indicators))]
    indicators_dict = dict.fromkeys(['date', 'well']+name)
    indicators_dict = {x: [] for x in indicators_dict.keys()}
    assos_dict = {x: y for x, y in zip(indicators, name)}
    start_date = datetime.datetime.strptime(start, '%d.%m.%Y')
    try:
        for m in kwarg['mod']:
            for w in kwarg['wells']:
                for t in kwarg['step']:
                    if t.to_datetime() >= start_date:
                        indicators_dict['date'].append(t.to_datetime())
                        indicators_dict['well'].append(w.name)
                        for i in indicators:
                            indicators_dict[assos_dict[i]].append(
                                i[m, w, t].to_list()[0])
                    else:
                        continue
    except Exception as e:
        m = kwarg['mod']
        for w in kwarg['wells']:
            for t in kwarg['step']:
                if t.to_datetime() >= start_date:
                    indicators_dict['date'].append(t.to_datetime())
                    indicators_dict['well'].append(w.name)
                    for i in indicators:
                        indicators_dict[assos_dict[i]].append(
                            i[m, w, t].to_list()[0])
                else:
                    continue
    result = pd.DataFrame(indicators_dict, index=indicators_dict['date'])
    return result.drop('date', axis=1)


def adapt_report_frame(frame, **kwarg):
    frame.columns = ['well', 'wlpt', 'wlpth', 'wopt', 'wopth']
    well_cum = frame.loc[frame.index == frame.index.max()]
    well_cum['lik_diff'] = (
        well_cum['wlpth']-well_cum['wlpt'])/well_cum['wlpth']*100
    well_cum['oil_diff'] = (
        well_cum['wopth']-well_cum['wopt'])/well_cum['wopth']*100
    well_cum['oil'] = pd.cut(
        well_cum['oil_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
    well_cum['lik'] = pd.cut(
        well_cum['lik_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
    final = {}
    final['user'] = getpass.getuser()
    final['model'] = [i.name for i in kwarg['mod']][0]
    final['date'] = datetime.datetime.now()
    final['total_wells'] = well_cum.loc[well_cum['wopth']
        > 0, 'well'].unique().shape[0]
    final['total_oil'] = well_cum['wopt'].sum()/well_cum['wopth'].sum()*100
    final['total_liq'] = well_cum['wlpt'].sum()/well_cum['wlpth'].sum()*100
    final['oil_adapt'] = well_cum.loc[well_cum['oil'] ==
        'good', 'wopth'].sum()/well_cum['wopth'].sum()*100
    final['liq_adapt'] = well_cum['lik'].value_counts(normalize=True)[1]*100
    final['wells_adapt'] = well_cum['oil'].value_counts(normalize=True)[1]*100
    return pd.DataFrame(final, index=[1])


def create_report_dir(path):
    '''Creates a result folder and sets it by default when writing files
        path = r let to the model's sensor'''
    if os.path.exists((path+r'\\reports')):
        os.chdir(path+r'\\reports')
    else:
        os.chdir(path)
        os.mkdir('reports')
        os.chdir(path+r'\\reports')

def interpolate_press_by_sipy(frame, a=2, b=0.1):
	b, a = signal.butter(a,b)
	if frame.shape[0]>12:
		frame.index=frame['date']
		frame['SBHPH']= signal.filtfilt(b, a, frame['BHPH'].interpolate(method='time').fillna(method='bfill')) 
		frame['STHPH']= signal.filtfilt(b, a, frame['THPH'].interpolate(method='time').fillna(method='bfill')) 
		frame.loc[frame['BHPH'].interpolate(method='time').isnull(), 'SBHPH'] = np.NaN
		frame.loc[frame['THPH'].interpolate(method='time').isnull(), 'STHPH'] = np.NaN
		frame.loc[(frame['status']=='not_work'), 'SBHPH'] = np.NaN
		frame.reset_index(drop=True, inplace=True)
	else:
		frame['SBHPH']= np.NaN 
		frame['STHPH']= np.NaN
	return frame
	
def interpolate_prod_by_sipy(frame, a=2, b=0.2):
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame['date']
        frame['SQLIQ'] = signal.filtfilt(
            b, a, frame['QLIQ'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[(frame['status'] == 'not_work'), 'SQLIQ'] = 0
        frame.loc[(frame['status'] == 'inj'), 'SQLIQ'] = 0
        frame.loc[(frame['SQLIQ'] < 0), 'SQLIQ'] = 0
        frame['SWCT'] = signal.filtfilt(
            b, a, frame['WCT'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[(frame['status'] == 'not_work'), 'SWCT'] = 0
        frame.loc[(frame['status'] == 'inj'), 'SWCT'] = 0
        frame.loc[(frame['SWCT'] < 0), 'SWCT'] = 0
        frame.reset_index(drop=True, inplace=True)
    else:
        frame['SQLIQ'] = np.NaN
        frame['SWCT'] = np.NaN
    return frame


def model_frame(**kwarg):
    df = dataframe_creater(
        woprh, wwprh, wwirh, wbhph, wthph, wlpr, wbhp, wbp9, start='01.01.1955', **kwarg)
    df = df.reset_index()
    df.columns = ['date', 'well', 'QOIL', 'QWAT',
                  'QWIN', 'BHPH', 'THPH', 'MQLIQ', 'MBHP', 'MPRES']
    return df

