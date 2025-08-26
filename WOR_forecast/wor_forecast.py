
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log
from scipy.optimize import curve_fit


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

    def set_hist_data(self, df: pd.DataFrame):
        """Переводим добычу в КИН"""
        Np = df['opt'].to_numpy()
        self.wcth = df['wct'].to_numpy()
        self.R = Np/self.N

    def sw_calc(self):
        """Расчитываем среднее насыщение как долю запасов пласта, отобранных и замещенных водой 
        Sw = Swav при значение lam=1, в противном случае происходит запаздывание насыщение 
        на фронте относительно среднего насыщения по пласту, что в общем то логично, если 
        вспомнить методику Велджа"""
        self.Swav = self.R*(1-self.Swi)+self.Swi
        self.Sw = self.lam*self.Swav+(1-self.lam)*(1-self.Sor)
        # self.Swd = (self.Sw-self.Swi)/(1-self.Swi-self.Sor)

    def lin_coef_calc(self, lam):
        """На основе из Бакл-Лев уравнения выводим коэффициенты для линизации уравнения"""
        self.x1 = np.log(lam*self.c*self.R+1-lam)
        self.x2 = np.log(lam - self.c*self.R+1*lam)

    def watercut_calc(self,lam, nw, no):
        """Считаем обводненность от КИН"""
        # self.sw_calc()
        self.lin_coef_calc(lam)
        self.wor = np.exp(self.a+nw*self.x1-no*self.x2) # wor calculationsо
        self.fw = 1-1/(self.wor+1)
        return self.fw

    def get_watercut(self):
        """Считаем обводненность от КИН"""
        frame = np.column_stack((self.R, self.Swav, self.Sw, self.fw))
        frame = pd.DataFrame(frame, columns=['R','Swav', 'Sw', 'fw'])
        return frame

    def wct_fitting(self):
        """Подгонка параметров модели к историческим данным"""
        # Определяем функцию для подгонки с правильной сигнатурой
        def fit_func(R, lam, nw, no):
            """Функция для curve_fit с правильными параметрами"""
            self.lin_coef_calc(lam)
            wor = np.exp(self.a + nw * self.x1 - no * self.x2)
            fw = 1 - 1 / (wor + 1)
            return fw
        
        # Задаем начальные значения параметров
        initial_guess = [self.lam, 1.0, 1.0]  # lam, nw, no
        
        # Задаем границы параметров (опционально)
        bounds = ([0.1, 0.1, 0.1], [2.0, 5.0, 5.0])  # нижние и верхние границы
        
        try:
            # Выполняем подгонку
            popt, pcov = curve_fit(
                fit_func, 
                self.R, 
                self.wcth, 
                p0=initial_guess,
                bounds=bounds,
                maxfev=10000  # увеличиваем количество итераций
            )
            
            # Обновляем параметры модели
            self.lam, self.nw, self.no = popt
            print(f"Оптимальные параметры: lam={popt[0]:.4f}, nw={popt[1]:.4f}, no={popt[2]:.4f}")
            
            return popt, pcov
            
        except Exception as e:
            print(f"Ошибка при подгонке: {e}")
            return None, None
    
    
        
    # %%
    df = pd.read_csv('/home/albert/Документы/decliner/test_data/test_wor_func.csv')
    field = WOR_forecaster(**{'Swi': 0.3, 
                              'Sor': 0.3,
                              'muo':2.47,
                              'muw':0.4,
                              'krw':0.3,
                              'kro':1,
                              'N': 18670*2,
                              'lam': 1.01})
    # df
    field.set_hist_data(df)
    field.R
