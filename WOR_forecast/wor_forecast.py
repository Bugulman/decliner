
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log


class WOR_forecaster():
    """docstring for ."""
    def __init__(self, **kwarg):
        self.Swi = kwarg['Swi']
        self.Sor = kwarg['Sor']
        self.muo = kwarg['muo']
        self.muw = kwarg['muw']
        self.krw = kwarg['krw']
        self.kro = kwarg['kro']
        self.lam = kwarg['lam']
        self.N = kwarg['N']
        self.M = (self.muo*self.krw)/(self.muw*self.kro)
        self.c = (1-self.Swi)/(1-self.Swi-self.Sor)
        self.a = log(self.M)

    def set_hist_data(self, Np):
        """Переводим добычу в КИН"""
        self.R = Np/self.N

    def sw_calc(self):
        """Расчитываем среднее насыщение как долю запасов пласта, отобранных и замещенных водой 
        Sw = Swav при значение lam=1, в противном случае происходит запаздывание насыщение 
        на фронте относительно среднего насыщения по пласту, что в общем то логично, если 
        вспомнить методику Велджа"""
        self.Swav = self.R*(1-self.Swi)+self.Swi
        self.Sw = self.lam*self.Swav+(1-self.lam)*(1-self.Sor)
        # self.Swd = (self.Sw-self.Swi)/(1-self.Swi-self.Sor)

    def lin_coef_calc(self):
        """На основе из Бакл-Лев уравнения выводим коэффициенты для линизации уравнения"""
        self.x1 = np.log(self.lam*self.c*self.R+1-self.lam)
        self.x2 = np.log(self.lam - self.c*self.R+1*self.lam)
        
    def get_watercut(self, nw, no):
        """Считаем обводненность от КИН"""
        self.sw_calc()
        self.lin_coef_calc()
        self.wor = np.exp(self.a+nw*self.x1-no*self.x2) # wor calculationsо
        self.fw = 1-1/(self.wor+1)
        frame = np.column_stack((self.R, self.Swav, self.Sw, self.fw))
        frame = pd.DataFrame(frame, columns=['R','Swav', 'Sw', 'fw'])
        return frame



    


# %%
field = WOR_forecaster(**{'Swi': 0.15, 
                          'Sor': 0.314,
                          'muo':20,
                          'muw':0.4,
                          'krw':0.3,
                          'kro':1,
                          'N': 5000,
                          'lam': 1.1})
field.set_hist_data(np.linspace(0,1000))
field.get_watercut(1,1)
