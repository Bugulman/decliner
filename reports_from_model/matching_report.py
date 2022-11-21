#Automaticaly recalculate=false
#Single model=false
#пишите здесь ваш ко
import getpass
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd 
import os

os.environ['TCL_LIBRARY'] = r'D:\other\my_software\python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\other\my_software\python\tcl\tk8.6'
  
keyword = {'grou':get_all_groups(), 
'wells':get_wells_from_filter ('Фильтр по скважинам 1'), 
'mod' : get_all_models(), 
'step':get_all_timesteps()} 

print('begin')
def dataframe_creater(*args, start='01.01.2000', **kwarg):
    """Function for converting navigation format to pandas dataframe
         *args - list of arguments to issue in the frame 
             dimens - well, here is one of two:
			well - for issuing a frame for wells
			group - for issuing by group"""
    indicators = [x for x in args]
    name = ['Parametr{}'.format(x) for x in range(0, len(indicators))]
    indicators_dict = dict.fromkeys(['date', 'well']+name)
    indicators_dict = {x:[] for x in indicators_dict.keys()} 
    assos_dict = {x:y for x,y in zip(indicators, name)}
    start_date = datetime.datetime.strptime(start, '%d.%m.%Y')
    for m in kwarg['mod']:
        for w in kwarg['wells']:
            for t in kwarg['step']:
                if t.to_datetime() >= start_date:
                    indicators_dict['date'].append(t.to_datetime())
                    indicators_dict['well'].append(w.name)
                    for i in indicators:
                        indicators_dict[assos_dict[i]].append(i[m,w,t].to_list()[0])
                else:
                    continue
    result = pd.DataFrame(indicators_dict, index = indicators_dict['date'])
    return result.drop('date', axis=1)

def create_report_dir(path):
    '''Creates a result folder and sets it by default when writing files
        path = r let to the model's sensor'''
    if os.path.exists((path+r'\\reports')):
        os.chdir(path+r'\\reports')
    else:
        os.chdir(path)
        os.mkdir('reports')
        os.chdir(path+r'\\reports')
        
        
create_report_dir(path = get_project_folder ( )) 
frame = dataframe_creater(wlprh, wlpr, woprh, wopr, wwirh, wwir, wlpth, wlpt, wopth, wopt, wwith, wwit, start='01.01.1955', **keyword)
#df = df.reset_index()


frame.columns=['well', 'wlprh', 'wlpr', 'woprh', 'wopr', 'wwirh', 'wwir', 'wlpth', 'wlpt', 'wopth', 'wopt', 'wwith', 'wwit']
fild_frame=frame.groupby(frame.index).sum()
ago = fild_frame.index.year.max()-5
limit = str(ago if ago in fild_frame.index.year else fild_frame.index.year.min())

frame.columns=['well', 'wlprh', 'wlpr', 'woprh', 'wopr', 'wwirh', 'wwir', 'wlpth', 'wlpt', 'wopth', 'wopt', 'wwith', 'wwit']
well_cum = frame.loc[frame.index == frame.index.max()]
well_cum['wlprh_diff'] = (well_cum['wlpth']-well_cum['wlpt'])/well_cum['wlpth']*100
well_cum['woprh_diff'] = (well_cum['wopth']-well_cum['wopt'])/well_cum['wopth']*100
well_cum['wwirh_diff'] = (well_cum['wwith']-well_cum['wwit'])/well_cum['wwith']*100
well_cum['woprh_mask'] = pd.cut(well_cum['woprh_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
well_cum['wlprh_mask'] = pd.cut(well_cum['wlprh_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
well_cum['wwirh_mask'] = pd.cut(well_cum['wwirh_diff'], [-1000, -20, 20.5, 1000], labels=['to_mach', 'good', 'poor'])
well_cum['wlprh_abs'] = (well_cum['wlpth']-well_cum['wlpt'])**2
well_cum['woprh_abs'] = (well_cum['wopth']-well_cum['wopt'])**2
well_cum['wwirh_abs'] = (well_cum['wwith']-well_cum['wwit'])**2
final={}
final['user'] = getpass.getuser()
final['model'] = [i.name for i in keyword['mod']][0]
final['date'] = datetime.datetime.now()
final['total_wells_prod'] = well_cum.loc[well_cum['wopth']>0, 'well'].unique().shape[0]    
final['total_wells_inj'] = well_cum.loc[well_cum['wwith']>0, 'well'].unique().shape[0]    
final['total_oil'] = well_cum['wopt'].sum()/well_cum['wopth'].sum()*100
final['total_liq'] = well_cum['wlpt'].sum()/well_cum['wlpth'].sum()*100
final['oil_adapt'] = well_cum.loc[well_cum['woprh_mask']=='good', 'wopth'].sum()/well_cum['wopth'].sum()*100
final['liq_adapt'] = well_cum['wlprh_mask'].value_counts(normalize=True)[1]*100
final['wells_adapt'] = well_cum['woprh_mask'].value_counts(normalize=True)[1]*100
title_frame = pd.DataFrame(final, index=[1])

oil = [i for i in frame.columns if 'op' in i]
liq = [i for i in frame.columns if 'lp' in i]
inj = [i for i in frame.columns if 'wi' in i]
oil_wells = [i for i in well_cum.columns if 'op' in i]
liq_wells = [i for i in well_cum.columns if 'lp' in i]
inj_wells = [i for i in well_cum.columns if 'wi' in i]
oil_wells.insert(0,'well')
liq_wells.insert(0,'well')
inj_wells.insert(0,'well')


def cum_graf(y):
    '''Create pic for field/
        y = dataframe from field'''
    fig = plt.figure(figsize=(15, 10)) 
    egrid = (4,3)
    ax1 = plt.subplot2grid(egrid, (0, 0), colspan=3)
    ax2 = plt.subplot2grid(egrid, (1, 0), rowspan=2, colspan=3)
    ax3 = plt.subplot2grid(egrid, (3, 0), colspan=2)
    ax4 = plt.subplot2grid(egrid, (3, 2))
    cum = [i for i in y.columns if 't' in i]
    rate = [i for i in y.columns if 'r' in i]
    hist = [i for i in rate if 'h' in i]
    model = [i for i in rate if 'h' not in i]
    
    last=y.loc[y.index.max().date()-pd.DateOffset(years=5):]
    ax1.plot(last[hist], color='k')
    ax1.plot(last[model], color='r')
    ax1.fill_between(last.index, last[hist[0]].values*1.1, last[hist[0]].values, where=last[hist[0]].values*1.2>last[hist[0]].values, facecolor='green', alpha=0.3)
    ax1.fill_between(last.index, last[hist[0]].values*0.9, last[hist[0]].values, where=last[hist[0]].values>last[hist[0]].values*0.8, facecolor='green', alpha=0.3)
    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('Rate/inj rate', fontsize=14)
    ax1.grid(True)
 
    ax2.plot(y[hist], color='k')
    ax2.plot(y[model], color='r')
    ax2.fill_between(y.index, y[hist[0]].values*1.2, y[hist[0]].values, where=y[hist[0]].values*1.2>y[hist[0]].values, facecolor='green', alpha=0.3)
    ax2.fill_between(y.index, y[hist[0]].values*0.8, y[hist[0]].values, where=y[hist[0]].values>y[hist[0]].values*0.8, facecolor='green', alpha=0.3)
    ax2.set_xlabel('Date', fontsize=14)
    ax2.set_ylabel('Rate/inj rate', fontsize=14)
    ax2.grid(True)
    hist2 = [i for i in cum if 'h' in i]
    model2 = [i for i in cum if 'h' not in i]
    ax3.plot(y[hist2], color='black')
    ax3.plot(y[model2], color='r')
    ax3.set_xlabel('Date', fontsize=14)
    ax3.set_ylabel('Cumulative prod/inj', fontsize=14)
    
    ax4.bar(1, y.loc[y.index.max(), hist2], 0.5, alpha=0.7, color='k')
    ax4.bar(2, y.loc[y.index.max(), model2], 0.5, alpha=0.7, color='r')
    int_adapt=(y.loc[y.index.max(), model2].values/y.loc[y.index.max(), hist2].values)
    ax4.text(2, y.loc[y.index.max(), model2].values/2, str(round(int_adapt[0], 2)), fontsize=20, va="center", ha="center")
    ax4.set_xticks([1,2])
    ax4.set_xticklabels(['History', 'Models'])
    fig.savefig(f'graf_{hist[0]}.png')


def frame_to_pdf(df, transponse=True, res_index=True):
    '''Convert dataframe format into list of list. Need fot past tables into pdf.
        transponse = transponse frame'''
    df = df.round(1).T if transponse==True else df.round(1)
    if res_index==True:
        title = [i for i in df.reset_index().columns]
    else:
        title = [i for i in df.columns]
    body = df.reset_index().values.tolist() if res_index==True else df.values.tolist()
    body.insert(0, title)
    return body 

def wells_graf(y):
    '''Create pic for wells/
        y = dataframe from wells'''
    fig = plt.figure(figsize=(15, 10)) 
    egrid = (4,2)
    ax1 = plt.subplot2grid(egrid, (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid(egrid, (2, 0),rowspan=2)
    ax3 = plt.subplot2grid(egrid, (2, 1),rowspan=2)
    cum = [i for i in y.columns if 't' in i]
    mask = [i for i in y.columns if 'mask' in i]
    hist = [i for i in cum if 'h' in i]
    model = [i for i in cum if 'h' not in i]
    bar_width = 0.8
    opacity = 0.6
    
    ax1.scatter(y[model], y[hist], s=10, edgecolors ='black')#, cmap='autumn', c=y[mask])
    ax1.plot(np.arange(y[model[0]].max()),np.arange(y[model[0]].max()), color='r')
    ax1.fill_between(np.arange(y[model[0]].max()), np.arange(y[model[0]].max())*1.2, np.arange(y[model[0]].max()),
                     where=np.arange(y[model[0]].max())*1.2>np.arange(y[model[0]].max()), facecolor='green', alpha=0.3)
    ax1.fill_between(np.arange(y[model[0]].max()), np.arange(y[model[0]].max())*0.8, np.arange(y[model[0]].max()),
                     where=np.arange(y[model[0]].max())>np.arange(y[model[0]].max())*0.8, facecolor='green', alpha=0.3)
    ax1.set_xlabel('History', fontsize=14)
    ax1.set_ylabel('Model', fontsize=14)
    ax1.grid(True)
    
    per_of_wells = y[mask[0]].value_counts(normalize=True)[1]*100
    per_of_total = y.loc[y[mask[0]].isin(['good']), hist].sum()/y.loc[y[mask[0]].isin(['to_mach', 'good', 'poor']), hist].sum()
    ax2.bar(1, per_of_total, bar_width, alpha=opacity, color='g')
    ax2.bar(2, 1-per_of_total, bar_width, alpha=opacity, color='r')
    ax2.set_xlabel('Matched cum hitory', fontsize=14)
    ax2.set_ylabel('Score', fontsize=14)
    ax2.set_xticks([1,2])
    ax2.set_xticklabels(('Mathed', 'Not matched'))
    ax2.text(1, per_of_total/2, str(round(per_of_total[0], 2)), fontsize=20, va="center", ha="center")
    ax2.text(2, (1-per_of_total)/2, str(round((1-per_of_total[0]),2)), fontsize=20, va="center", ha="center")
    
    ax3.bar(1, per_of_wells, bar_width, alpha=opacity, color='g')
    ax3.bar(2, 100-per_of_wells, bar_width, alpha=opacity, color='r')
    ax3.set_xlabel('% wells matched', fontsize=14)
    ax3.set_ylabel('Score', fontsize=14)
    ax3.set_xticks([1,2])
    ax3.set_xticklabels(('Mathed', 'Not matched'))
    ax3.text(1, per_of_wells/2, str(round(per_of_wells, 1)), fontsize=20, va="center", ha="center")
    ax3.text(2, (100-per_of_wells)/2, str(round((100-per_of_wells),1)), fontsize=20, va="center", ha="center")
    fig.savefig(f'wells_{hist[0]}.png')

def wells_reiting(y):
    '''Create table for field/
        y = dataframe from wells'''
    hist = [i for i in y.columns if 'h' in i]
    mask = [i for i in y.columns if 'mask' in i]
    otn_diff = [i for i in y.columns if 'diff' in i]
    abs_diff = [i for i in y.columns if 'abs' in i]
    worst = y.sort_values(by=abs_diff, ascending=False).head(10)
    nearest = y.loc[(y[otn_diff[0]].between(20, 25))|(y[otn_diff[0]].between(-25,-20))].sort_values(by=hist[0], ascending=False).head(10)
    lost = y.loc[(y[otn_diff[0]]==100), 'well'].values.tolist()
    return worst.iloc[:,:-1], nearest.iloc[:,:-1], lost

def field_table(y, start_date=limit):
    '''Create table for field/
        y = dataframe from field'''
    hist = [i for i in y.columns if 'h' in i]
    model = [i for i in y.columns if 'h' not in i]
    agg_dict=dict.fromkeys(y.columns)
    for x in y.columns:
        if 'r' in x:
            agg_dict[x]=np.mean
        else:
            agg_dict[x]=np.sum
    y = y.loc[start_date:].pivot_table(index=y[start_date:].index.year, aggfunc=agg_dict)
    for m, h in zip(model, hist):
        y['diff/n'+m]=(y[m]-y[h])/y[h]*100
    return y.round(1)
    
 

from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors

file = SimpleDocTemplate('HM_report.pdf', pagesize=A4)
flow = []
styles = getSampleStyleSheet()
title_tab=TableStyle([
    ("GRID", (0,0), (-1,-1),1, colors.gray),
    ("FONT", (0,0), (-1,-1),"Times-Italic",7),
    ('BACKGROUND', (0,0), (-1,0), colors.lightyellow)
])
tab_style=TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.green),
    ("FONT", (0,0), (-1,-1),"Times-Italic",7)
])

text = Paragraph('<u>HISTORY</u><br></br>MATCHING REPORT', style=styles["Normal"])
title=Table(frame_to_pdf(title_frame, transponse=False)) ##add tible at the top of page
title.setStyle(title_tab)
    
for field, wells, names in zip([oil, liq, inj], [oil_wells, liq_wells, inj_wells],['oil', 'liquid', 'water injection']):
    flow.append(text)
    flow.append(Spacer(1, 1))
    flow.append(title)
    name = Paragraph(f"<font size=14> Field report by <u>{names}</u></font>")
    flow.append(name)
    flow.append(Spacer(1, 6))
    cum_graf(frame.groupby(frame.index)[field].sum())
    pic = Image(f'graf_{field[0]}.png', width=500, height=350)
    flow.append(pic)
    some = field_table(fild_frame[field])
    year=[some.index.max()-5]
    totable=frame_to_pdf(some, transponse=False)
    table = Table(totable)
    table.setStyle(tab_style)
    flow.append(table)
    flow.append(PageBreak())
    
    flow.append(text)
    flow.append(Spacer(1, 1))
    flow.append(title)
    name = Paragraph(f"<font size=14> Wells report by <u>{names}</u></font>")
    flow.append(name)
    flow.append(Spacer(1, 6))
    wells_graf(well_cum[wells])
    pic = Image(f'wells_{wells[3]}.png', width=500, height=300)
    flow.append(pic)
    analitic_tables = wells_reiting(well_cum[wells])
    flow.append(Spacer(0, 2))
    lost_wells=Paragraph(f'We find <b>{len(analitic_tables[2])}</b> wells that do not work in model<br></br>\
                         The nomber is: {[str(i) for i in analitic_tables[2]]}', style=styles["Normal"]   )
    flow.append(lost_wells)
    flow.append(Spacer(0, 2))
    table_name = Paragraph('<font color = "red"><u>TOP 10 worst matched wells</u></font>')
    flow.append(table_name)
    worst = Table(frame_to_pdf(analitic_tables[0], transponse=False, res_index=False), style=title_tab, rowHeights=11)
    flow.append(worst)
    flow.append(Spacer(0, 2))
    table_name = Paragraph('<font color = "green"><u>TOP 10 candidates to match</u></font>')
    flow.append(table_name)
    near = Table(frame_to_pdf(analitic_tables[1], transponse=False, res_index=False), style=title_tab, rowHeights=11)
    flow.append(near)
    
    flow.append(PageBreak())
file.build(flow)
print('end')