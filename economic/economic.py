#Automaticaly recalculate=true
#Single model=false
# Automaticaly recalculate=true
# Single model=false
# Automaticaly recalculate=false
# Single model=false
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import transliterate
import pandas as pd
import oily_report as olr
import win32com.client
import shutil
import math
import datetime
from datetime import date
import os
os.environ["PATH"] = r"d:\other\my_software\python\Lib\site-packages\pywin32_system32\;" + os.environ["PATH"]


start = 2020  # ???? ?????? ????????
den = 0.862

folder_path = get_project_folder()

res_graph = graph(type='field', default_value=math.nan)


def dataframe_creater(*args, start='01.01.2000', **kwarg):
    """Function for converting navigation format to pandas dataframe
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


def fond_analizator(frame, oil_dens=0.865, wat_dens=1.05):
    frame['drilled_p'] = (frame['shifted'] == 0) & (frame['lpr'] > 0)
    frame['drilled_i'] = (frame['shifted'] == 0) & (frame['wir'] > 0)
    frame['GTM'] = (frame['opr']/frame['opr'].shift(1) > 1.3)
    frame['VNS'] = (frame['drilled_i'] == False) & (frame['wir'].shift(1) == 0) & (frame['wir'].shift(2) == 0) & (frame['wir'].shift(3) == 0)\
        & (frame['wir'].shift(4) == 0) & (frame['wir'].shift(5) == 0) & (frame['wir'].shift(6) == 0)\
        & (frame['wir'].shift(7) == 0) & (frame['wir'].shift(8) == 0) & (frame['wir'].shift(9) == 0)\
        & (frame['wir'].shift(10) == 0) & (frame['wir'].shift(11) == 0) & (frame['wir'].shift(12) == 0)\
        & (frame['wir'] > 0)
    frame['VDS'] = (frame['drilled_p'] == False) & (frame['lpr'].shift(1) == 0) & (frame['lpr'].shift(2) == 0) & (frame['lpr'].shift(3) == 0)\
        & (frame['lpr'].shift(4) == 0) & (frame['lpr'].shift(5) == 0) & (frame['lpr'].shift(6) == 0)\
        & (frame['lpr'].shift(7) == 0) & (frame['lpr'].shift(8) == 0) & (frame['lpr'].shift(9) == 0)\
        & (frame['lpr'].shift(10) == 0) & (frame['lpr'].shift(11) == 0) & (frame['lpr'].shift(12) == 0)\
        & (frame['lpr'] > 0)
    frame['prod'] = (frame['date'].dt.month == 12) & (frame['lpr'] > 0)
    frame['inj'] = (frame['date'].dt.month == 12) & (frame['wir'] > 0)
    frame['year_oil'] = (frame['date'].dt.month == 12) & (frame['wir'] > 0)
    frame['year_liq'] = (frame['date'].dt.month == 12) & (frame['wir'] > 0)
    frame['year_wat'] = (frame['date'].dt.month == 12) & (frame['wir'] > 0)
    frame['month_oil'] = frame['opt'].diff()
    frame['month_oil'].fillna(frame['opt'].min(), inplace=True)
    frame['month_liq'] = frame['lpt'].diff()
    frame['month_liq'].fillna(frame['lpt'].min(), inplace=True)
    frame['month_inj'] = frame['wit'].diff()
    frame['month_inj'].fillna(frame['wit'].min(), inplace=True)
    frame['frack'] = (frame['shifted_P'] > 0) &\
        (frame['press']-frame['bhp'] > 0.1) &\
        (frame['opr']/frame['opr'].shift(1) > 1.1) &\
        (frame['lpr'] > 0) & (frame['prodaction']/frame['shifted_P'] > 1.2)
    frame['MUN_VIR'] = (frame['shifted_P'] > 0) & (frame['prodaction'] > 0) & (frame['lpr'] > 0) &\
        (frame['press']-frame['bhp'] > 0.1) &\
        (frame['frack'].shift(1) != True) &\
        (frame['lpr'].shift(1) != 0) &\
        (frame['bhp'] > 0) & (
        frame['prodaction']/frame['shifted_P'] < 0.6)
    frame['MUN_nag'] = (frame['shifted_P'] > 0) & (frame['wir'] > 0) &\
        (frame['wir'].shift(1) != 0) &\
        (frame['bhp'] > 0) & (frame['prodaction']/frame['shifted_P'] < 0.6) &\
        (frame['prodaction']/frame['shifted_P'] > 1.2)
    frame['MUN_OTKL'] = (frame['shifted_P'] > 0) & (frame['wir'] > 0) &\
                        (frame['wir'].shift(1) != 0) &\
                        (frame['prodaction']/frame['shifted_P'] < 0.8)
    frame['KRS_GNO'] = (frame['shifted_P'] > 0) & (
        frame['opr']/frame['lpr'].shift(1) > 1.2) & (frame['prodaction']/frame['shifted_P'] < 1.2)
    return frame


def monthly_prod(frame, oil_dens=0.862, wat_dens=1):
    frame['нефть, тыс.т/год'] = frame['opt'].diff()/1000*oil_dens
    frame['нефть, тыс.т/год'].fillna(frame['opt'].min() /
                                                 1000*oil_dens, inplace=True)
    frame['жидкость, тыс.м3/год'] = frame['lpt'].diff()/1000
    frame['жидкость, тыс.м3/год'].fillna(
        frame['lpt'].min(), inplace=True)
    frame['вода, тыс.м3/год'] = frame['wpt'].diff()/1000
    frame['вода, тыс.м3/год'].fillna(
        frame['wpt'].min(), inplace=True)
    frame['газ, тыс.м3/год'] = frame['gpt'].diff()/1000
    frame['газ, тыс.м3/год'].fillna(frame['gpt'].min(), inplace=True)
    frame['газовый фактор, м3/м3'] = frame['газ, тыс.м3/год'] / \
        (frame['нефть, тыс.т/год']/oil_dens)
    frame['закачка, тыс.м3/год'] = frame['wit'].diff()/1000
    frame['закачка, тыс.м3/год'].fillna(
        frame['wit'].min(), inplace=True)
    cum = [i for i in frame.columns if 't' in i]
    frame.drop(columns=cum, inplace=True)
    return frame


def economic_frame():
    """TODO: Docstring for economic_frame.
    :returns: TODO
    """
    df = dataframe_creater(wlpt, wlpr, wopt, wopr, wwir, wwit, wbp9,
                           wbhp, wpio, wpiw, start='01.01.2020', **keyword).reset_index()
    df.columns = ['date', 'well', 'lpt', 'lpr', 'opt',
                  'opr', 'wir', 'wit', 'press', 'bhp', 'pio', 'piw']
    df['shifted'] = df['lpt'].shift(
        1, fill_value=0)+df['wit'].shift(1, fill_value=0)
    df['prodaction'] = df['pio']+df['piw']
    df['shifted_P'] = df['prodaction'].shift(1, fill_value=0)
    df['date'] = pd.to_datetime(df['date'])
    df = pd.DataFrame(df.groupby(by='well').apply(fond_analizator))
    agg_dict = {'month_liq': 'sum', 'month_oil': 'sum', 'month_inj': 'sum', 'prod': 'sum', 'inj': 'sum', 'drilled_p': 'sum',
                'drilled_i': 'sum', 'GTM': 'sum', 'VNS': 'sum', 'VDS': 'sum', 'frack': 'sum', 'MUN_VIR': 'sum', 'MUN_nag': 'sum',
                'MUN_OTKL': 'sum', 'MUN_OTKL': 'sum', 'KRS_GNO': 'sum'}

    almost_all = df.loc[:, ['date', 'month_liq', 'month_oil', 'month_inj', 'prod', 'inj', 'drilled_p', 'drilled_i', 'GTM', 'VNS', 'VDS',
                            'frack', 'MUN_VIR', 'MUN_nag', 'MUN_OTKL', 'KRS_GNO']]\
        .groupby(df['date'].dt.year).agg(agg_dict)
    return almost_all.reset_index()


def surf_frame():
    """TODO: Docstring for surf_frame.
    :returns: TODO
    """
    dk_frame = dataframe_creater(
        glpt, gwpt, gopt, ggpt, gwit, start='01.01.2020', **keyword).reset_index()
    dk_frame.columns = ['date', 'group', 'lpt', 'wpt', 'opt', 'gpt', 'wit']
    dk_frame['date'] = pd.to_datetime(dk_frame['date'])
    dk_frame.set_index(['date'], inplace=True)
    dk_frame = dk_frame[dk_frame['group'].str.match(
        'MINN|DNS*|GZU*|KNS*|MTP|TTP')]
    dk_frame = pd.DataFrame(dk_frame.groupby(by='group').apply(monthly_prod))
    dk_frame['group'] = dk_frame['group'].apply(
        lambda x: transliterate.translit(x, 'ru'))
    # .stack().unstack(1)#.to_excel('frame_rem.xlsx')j
    noGOR = dk_frame.groupby('group').apply(lambda x: x.resample('1y').sum())
    noGOR['газовый фактор, м3/м3'] = noGOR['газ, тыс.м3/год'] / \
        (noGOR['нефть, тыс.т/год']/0.862)
    return noGOR.stack().unstack(1).reset_index()


# ??? ??????? ??????
name_fix = get_all_models()[0].name
# m = get_all_models()[1]

# copy sample of Excel file
excel_file_path = r'D:\project\Minnib_project\SCHED_PATTERNS\reports\ECONOMIC\Minnib.xlsx'

excel_file_new = 'Economic_model_' + str(name_fix).replace('/', '_') + '.xlsx'
print(1)
# create frame from model data
olr.create_report_dir(get_project_folder())
excel_file_path_new = str('D:/project\Minnib_project/SCHED_PATTERNS/reports/ECONOMIC/' + excel_file_new)
shutil.copyfile(excel_file_path, excel_file_path_new)
# write to Excel file
excel = win32com.client.Dispatch("Excel.Application")
excel.DisplayAlerts = False
wb = excel.Workbooks.Open(excel_file_path_new, UpdateLinks=False)
print(1)
# ??????? ?????? ????? Excel
tnav_sheet = excel.Sheets('tNavigator')
econ_sheet = excel.Sheets('Расчет (базовый+ГТМ)')
surf_sheet = excel.Sheets('Surf')
# ?????? ?????? ? Excel
tnav_sheet.Cells(1, 2).Value = name_fix

keyword = {'grou': get_all_groups(),
           'wells': get_group_by_name ('MINN').all_wells,
           'mod': get_model_by_name(name_fix),
           'step': get_all_timesteps()}
results = economic_frame().values.tolist()
print(3)

keyword = {'grou': get_all_groups(), 'wells': get_all_groups(),
           'mod':  get_model_by_name(name_fix), 'step': get_all_timesteps()}
           
results_surf = surf_frame().values.tolist()


cell_1 = tnav_sheet.Cells(4, 2)
cell_2 = tnav_sheet.Cells(cell_1.Row + len(results) - 1,
                          cell_1.Column + len(results[0]) - 1)
tnav_sheet.Range(cell_1, cell_2).Value = results

cell_1 = surf_sheet.Cells(4, 2)
cell_2 = surf_sheet.Cells(
    cell_1.Row + len(results_surf) - 1, cell_1.Column + len(results_surf[0]) - 1)
surf_sheet.Range(cell_1, cell_2).Value = results_surf

print(3)
# ?????? ? ???????????
BCR_row = 98
BCR_col = 23
BCR_cell = econ_sheet.Cells(BCR_row, BCR_col)

# ???????? ???????? ?????????? (BCR) ?? Excel
bcr_value = float(BCR_cell.Value)
print(bcr_value)

# ????????? ????
wb.Close(SaveChanges=True)

# ?????????? ???????????? ???????? BCR ? ?????? ?? ????????? ????
first_step = get_all_timesteps()[0]
last_step = get_all_timesteps()[-1]
res_graph[first_step] = 0
res_graph[last_step] = bcr_value

# ??????? ???????
export(res_graph, name='Benefit-Cost Ratio ')

print("Excel is ready!")
