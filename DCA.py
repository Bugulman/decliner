#Automaticaly recalculate=true
#Single model=false
#!/usr/bin/env python3
import pandas as pd
import h5py
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


def MH(time, qi, Di, bi, Dterm):
    Dterm = Di*Dterm
    m = dca.MH(qi=qi, Di=Di, bi=bi, Dterm=Dterm)
    return m.rate(time)


def dec_predict(frame):
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
        qi, Di = curve_fit(MH, sub['Time'], np.array(sub['SOIL']), bounds=(0, [100, 0.5, 0.5, 0.7]), method='trf')
    except ValueError:
        print(f'Ошибка определения темпа для скважины {name}')
        qi=[last_deb, 0.2, 0.2, 0.99] 
    except RuntimeError:
        print(f'Ошибка определения темпа для скважины {name}')
        qi=[last_deb, 0.2, 0.2, 0.99] 
    except:
        qi, Di = curve_fit(MH, sub['Time'], np.array(sub['SOIL']), bounds=(0, [100, 0.2, 0.2, 0.99]), method='dogbox')
    logging.info(f'Скважина {name[0]},начало прогноза-{sub.date.min()}, qi-{round(qi[0],2)} Di-{round(qi[1],2)}')
    qi[3]=qi[1]*qi[3]
    mh = dca.MH(*qi)
    prog = pd.DataFrame(np.concatenate((sub.date, pd.date_range(sub.date.max(), periods=120, freq='MS')[1:])))#[1:]
    prog.columns=['date']
    prog['Time'] = prog['date']-prog['date'].min()
    prog['Time'] = prog['Time'] / np.timedelta64(1, "D")
    prog['rate'] = mh.rate(prog.Time)
    prog['month_prod'] = mh.monthly_vol(prog.Time)
    frame=pd.merge(frame, prog, left_on='date', right_on ='date', how='outer')
    frame['well'].fillna(method='ffill', inplace=True)
    return frame
