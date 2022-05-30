#Automaticaly recalculate=true
#Single model=false
#!/usr/bin/env python3
import pandas as pd
import oily_report as olr
import pandas as pd
import datetime
import os
import numpy as np
from scipy import signal
import transliterate
from petbox import dca
from scipy.optimize import curve_fit
import logging
import matplotlib.pyplot as plt


def MH(time, qi, Di, bi, Dterm):
    Dterm = Di*Dterm
    m = dca.MH(qi=qi, Di=Di, bi=bi, Dterm=Dterm)
    return m.rate(time)

logging.disable()
def declane_fit(frame):
    frame = frame.loc[(frame['date']>'2010')&(frame.status=='prod'), ['well', 'date', 'SOIL', 'QOIL']]
    name = frame['well'].unique()
    frame['Time'] = frame['date']-frame['date'].min()
    frame['Time'] = frame['Time'] / np.timedelta64(1, "D")
    shift = frame.loc[frame['QOIL']==frame['QOIL'].max(), 'Time']
    shift = int(shift.head(1).values)
    frame['Time']=frame['Time']-shift
    sub=frame.copy()
    sub=sub[sub['Time']>=0]
    frame['Time']=frame['Time']+shift
    last_deb = float(frame['QOIL'].tail(1))
    try:
        qi, Di = curve_fit(MH, sub['Time'], np.array(sub['SOIL']), bounds=(0, [100, 0.2, 0.2, 0.99]), method='trf')
    except ValueError:
        print(f'Ошибка определения темпа для скважины {name}')
        qi=[last_deb, 0.2, 0.2, 0.99] 
    except RuntimeError:
        print(f'Ошибка определения темпа для скважины {name}')
        qi=[last_deb, 0.2, 0.2, 0.99] 
    except:
        qi, Di = curve_fit(MH, sub['Time'], np.array(sub['SOIL']), bounds=(0, [100, 0.2, 0.2, 0.99]), method='dogbox')
    qi[3]=qi[1]*qi[3]
    logging.info(f'Скважина {name[0]},начало прогноза-{sub.date.min()}, qi-{round(qi[0],2)} Di-{round(qi[1],2)}, {qi}')

    pivot_info = {'well':name[0],'first_date':sub.date.min(), 'qi':qi} 
    # pivot_info = {'well':name[0],'first_date':sub.date.min(), 
                  # 'qi':round(qi[0],2), 'Di':round(qi[1],2), 'bi':round(qi[2],2), 'Dterm':round(qi[3], 2)}
    pivot_info = pd.DataFrame([pivot_info])
    return pivot_info


def prod_predict(start, qi, long=120):
    mh = dca.MH(*qi)
    prog = pd.DataFrame(pd.date_range(start, periods=long, freq='MS')) 
    prog.columns=['date']
    prog['Time'] = prog['date']-prog['date'].min()
    prog['Time'] = prog['Time'] / np.timedelta64(1, "D")
    prog['rate'] = mh.rate(prog.Time)
    prog['month_prod'] = mh.monthly_vol(prog.Time)
    # frame=pd.merge(frame, prog, left_on='date', right_on ='date', how='outer')
    # frame['well'].fillna(method='ffill', inplace=True)
    return prog['rate']


def predict_viz(df_g, start, qi, long=120):#, last):
    """Для визуализации подобранных кривых падения"""
    fig = plt.figure(figsize=(10, 10));
    plt.subplot(211)
    #plt.axis([0, 110, 0, np.max(prodaction)])
    plt.plot(df_g['Дата'], df_g['QOIL'], color='grey', alpha = 0.75, label = 'prodaction')
    predict_range=pd.DataFrame(pd.date_range(start, periods=long, freq='MS')) 
    predict = prod_predict(start, qi, long=120)
    plt.plot(predict_range, predict, 'r--', color='blue', alpha = 0.8, label = 'hyperbolic')
    # plt.axvspan(first, last, facecolor='#2ca02c', alpha=0.1, label = 'trening_period')
    plt.grid(True)
    #plt.xlim(0, 20)
    plt.xlabel('Месяц работы', fontsize =20)
    plt.ylabel('Дебит нефти, т/сут', fontsize =20)
    plt.legend()
    #plt.text(2, np.max(typical_well['q_oil'])/12, 'b={0}\nD={1}\nq={2}'.format(round(b,2), round(D,2), round(q_first,1)), size = 12);
    #plt.savefig('Arps.png', bbox_inches='tight', dpi=600)
    
    plt.subplot(212)
    #cum_bef_forecast = np.cumsum(df_g['q_oil']*28).shift(2).fillna(0)[first]
    plt.plot(df_g['date'], np.cumsum(df_g['QOIL']*28), color='grey', alpha = 0.75, label = 'prodaction');
    plt.plot(predict_range, np.cumsum(predict*28), color='blue', alpha = 0.8, label = 'hyperbolic');
    plt.xlabel('месяц работы', fontsize = 20);
    plt.ylabel('интегральный дебит нефти', fontsize = 20);
    #plt.xlim(0, 20)
    plt.legend()    
    plt.show()
