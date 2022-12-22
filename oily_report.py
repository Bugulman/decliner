import getpass
import os
from datetime import datetime
import numpy as np
import pandas as pd
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
    start_date = datetime.strptime(start, '%d.%m.%Y')
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


def df_from_histtab(paramert_list: list, start='01.01.1950', **kwarg):
    """создает pandas Dataframe с данными из таблицы с историей в дизайнере модели.
    paramert_list - параметры для выгрузки, полный список можно получить через get_production_types
    keyword = {'wells': get_well_filter_by_name (name='14').get_wells (), требуемый список скважин
           'mod': get_all_wells_production_tables ()[0], таблица с данными по исптории
           'step': get_all_timesteps()}
    """

    from datetime import datetime

    import pandas as pd
    df = []
    coll_name = ['well', 'date']+paramert_list
    start_date = datetime.strptime(start, '%d.%m.%Y')
    for w in kwarg['wells']:
        print(w.name)
        for t in kwarg['mod'].get_records(well=w):
            if t.get_date().date() >= start_date.date():
                row = []
                row.append(w.name)
                row.append(t.get_date().date())
                row = row+[t.get_value(type=parametr)
                           for parametr in paramert_list]
                df.append(row)
            else:
                continue
    print(coll_name)
    result = pd.DataFrame(df, columns=coll_name)
    result.set_index('date', inplace=True)
    result.sort_values(by=['well', 'date'], ascending=True, inplace=True)
    return result


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
    final['date'] = datetime.now()
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
    '''функция сглаживает давление по DataFrame. Коэффициенты a и b для настройки.
      Чем выше a и ниже b тем сильнее сглаживание.
    '''
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame['date']
        frame['SBHPH'] = signal.filtfilt(
            b, a, frame['BHPH'].interpolate(method='time').fillna(method='bfill'))
        frame['STHPH'] = signal.filtfilt(
            b, a, frame['THPH'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[frame['BHPH'].interpolate(
            method='time').isnull(), 'SBHPH'] = np.NaN
        frame.loc[frame['THPH'].interpolate(
            method='time').isnull(), 'STHPH'] = np.NaN
        frame.loc[(frame['status'] == 'not_work'), 'SBHPH'] = np.NaN
        frame.reset_index(drop=True, inplace=True)
    else:
        frame['SBHPH'] = np.NaN
        frame['STHPH'] = np.NaN
    return frame


def interpolate_prod_by_sipy(frame, a=2, b=0.2, gas=False):
    '''функция сглаживает добычу по DataFrame. Коэффициенты a и b для настройки. 
      Чем выше a и ниже b тем сильнее сглаживание.
    '''
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12 and gas == False:
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
    elif frame.shape[0] > 12 and gas == True:
        frame.index = frame['date']
        frame['SQLIQ'] = signal.filtfilt(
            b, a, frame['QLIQ'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[(frame['status'] == 'not_work'), 'SQLIQ'] = 0
        frame.loc[(frame['status'] == 'inj'), 'SQLIQ'] = 0
        frame.loc[(frame['SQLIQ'] < 0), 'SQLIQ'] = 0
        frame['SWCT'] = signal.filtfilt(
            b, a, frame['WCT'].interpolate(method='time').fillna(method='bfill'))
        frame['SGOR'] = signal.filtfilt(
            b, a, frame['GOR'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[(frame['status'] == 'not_work'), ['SWCT', 'SGOR']] = 0
        frame.loc[(frame['status'] == 'inj'), ['SWCT', 'SGOR']] = 0
        frame.loc[(frame['SWCT'] < 0), ['SWCT', 'SGOR']] = 0
    else:
        frame['SQLIQ'] = np.NaN
        frame['SWCT'] = np.NaN
        frame['SGOR'] = np.NaN
    return frame


def prod_smooth(frame, a=15, b=0.1):
    '''функция сглаживает продуктивность по DataFrame. 
      Чем выше a и ниже b тем сильнее сглаживание.
    '''
    b, a = signal.butter(a, b)
    if frame.shape[0] > 12:
        frame.index = frame['date']
        frame.loc[(frame['SPROD'] < 0), 'SPROD'] = np.NaN
        frame.loc[(frame['SPROD'] > frame['SPROD'].quantile(0.8)),
                  'SPROD'] = np.NaN
        frame.loc[(frame['SPROD'] < frame['SPROD'].quantile(0.2)),
                  'SPROD'] = np.NaN
        frame['SPROD'] = signal.filtfilt(
            b, a, frame['SPROD'].interpolate(method='time').fillna(method='bfill'))
        frame.loc[(frame['status'] == 'not_work'), 'SPROD'] = 0
        frame.loc[(frame['status'] == 'inj'), 'SPROD'] = 0
        temp = frame['SPROD'].groupby(frame.index.year).agg('median')
        temp.name = 'PROD_AV'
        frame = pd.merge(frame, temp, left_on=frame.index.year,
                         right_on=temp.index)
        frame.reset_index(drop=True, inplace=True)
    else:
        frame['SPROD'] = np.NaN
    return frame


def histor_smoothing(df, gas=False):
    """Relives and smoothes pressure in source data
    :df:panda DataFrame with well production data. Should contain well|data|oil_rate|water_rate|
    gas_rate(optional)|water_injection|bottemhole_pressure|pres_meash
    :returns: pandas DataFrame with smoothing press
    """
    if gas == False:
        df.columns = ['date', 'well', 'QOIL', 'QWAT',
                      'QWIN', 'BHPH', 'THPH']
    else:
        df.columns = ['date', 'well', 'QOIL', 'QWAT', 'QGAS'
                      'QWIN', 'BHPH', 'THPH']
        df['GOR'] = df['QGAS']/df['QOIL']

    df['QLIQ'] = df['QOIL']+df['QWAT']
    df['WCT'] = (df['QLIQ']-df['QOIL'])/df['QLIQ']
    df['status'] = 'prod'
    df.loc[df['QWIN'] > 0, 'status'] = 'inj'
    df.loc[((df['QWIN'] == 0) & (df['QLIQ'] == 0)), 'status'] = 'not_work'
    df['THPH'] = df['THPH'].replace([-999, 0], np.nan)
    df['BHPH'] = df['BHPH'].replace([-999, 0], np.nan)
    df.loc[((df['BHPH'] > df['THPH']) & (df['status'] == 'prod')), 'THPH'] = np.NaN
    df = pd.DataFrame(df.groupby(by='well').apply(interpolate_press_by_sipy))
    df.reset_index(drop=True, inplace=True)
    if gas == False:
        df = pd.DataFrame(df.groupby(by='well').apply(
            interpolate_prod_by_sipy))
    else:
        df = pd.DataFrame(df.groupby(by='well').apply(
            interpolate_prod_by_sipy, gas=True))
    df.reset_index(drop=True, inplace=True)
    df['SOIL'] = df['SQLIQ']*(1-df['SWCT'])
    df['SPROD'] = df['SQLIQ']/(df['STHPH']-df['SBHPH'])
    df['PROD'] = df['QLIQ']/(df['THPH']-df['BHPH'])
    df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
    df['SPROD'] = df['SQLIQ']/(df['STHPH']-df['SBHPH'])
    df['PROD'] = df['QLIQ']/(df['THPH']-df['BHPH'])
    df = pd.DataFrame(df.groupby(by='well').apply(prod_smooth))
    df.reset_index(drop=True, inplace=True)
    df.loc[df['QLIQ'].isnull(), 'SPROD'] = np.NaN
    df['SBHPH'] = df['STHPH']-(df['SQLIQ']/df['PROD_AV'])
    df.loc[(df['SBHPH'] <= 0), 'SBHPH'] = np.NaN
    df['SBHPH'].fillna(method='bfill')
    return df


def model_frame(**kwarg):
    df = dataframe_creater(
        woprh, wwprh, wwirh, wbhph, wthph, wlpr, wbhp, wbp9, start='01.01.1955', **kwarg)
    df = df.reset_index()
    df.columns = ['date', 'well', 'QOIL', 'QWAT',
                  'QWIN', 'BHPH', 'THPH', 'MQLIQ', 'MBHP', 'MPRES']
    return df
