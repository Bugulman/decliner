
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import exp, log
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

    def sw_calc(self, OR):
        """Расчитываем среднее насыщение"""
        Swav = OR*(1-self.Swi)+self.Swi
        Sw = self.lam*Swav+(1-self.lam)*(1-self.Sor)
        return Swav, Sw

    def lin_coef_calc(self, lam, R):
        """На основе из Бакл-Лев уравнения выводим коэффициенты для линизации уравнения"""
        # Защита от отрицательных значений под логарифмом
        term1 = lam * self.c * R + 1 - lam
        term2 = lam - self.c * R * lam  # Исправленная формула
        
        # Обеспечиваем положительные значения для логарифма
        term1 = np.maximum(term1, 1e-10)  # минимальное положительное значение
        term2 = np.maximum(term2, 1e-10)  # минимальное положительное значение
        
        x1 = np.log(term1)
        x2 = np.log(term2)
        
        return x1, x2

    def watercut_from_wor(self, R, lam, nw, no):
        """Считаем обводненность от КИН"""
        x1, x2 = self.lin_coef_calc(lam, R)
        wor = np.exp(self.a + nw * x1 - no * x2)
        fw = 1 - 1 / (wor + 1)
        return fw

    def get_watercut(self):
        """Считаем обводненность от КИН"""
        self.wct_fitting()
        fw_model = self.watercut_from_wor(self.R, self.lam_fit, self.nw_fit, self.no_fit)
        Swav, Sw = self.sw_calc(self.R)
        frame = np.column_stack((self.R, Swav, Sw, fw_model, self.wcth))
        frame = pd.DataFrame(frame, columns=['R','Swav', 'Sw', 'fw_model','fw_hist'])
        return frame

    def limit_calc(self,nw, no, fw):
        exp_coeff = (3.5 * nw + 6.5 * no) / (nw + no)
        power_coeff = (1.3 * nw + 0.7 * no) / (nw * (nw + no))
        term1 = 1+0.006738*np.exp(exp_coeff)
        wor_ratio = (1/self.M) * (fw/(1 - fw))
        term2 = term1 * np.power(wor_ratio, power_coeff)
        d = term2**(nw/no)
        self.R_lim = 1/self.c*(1-1/d)
        return self.R_lim

    def wct_forecast(self):
        self.wct_fitting()
        R_lim = self.limit_calc(self.nw_fit, self.no_fit, 0.98)
        RF_predict = np.linspace(self.R.max(), R_lim+0.1)
        fw_predict = self.watercut_from_wor(RF_predict, self.lam_fit, self.nw_fit, self.no_fit)
        Swav_predict, Sw_predic = self.sw_calc(RF_predict)
        hist_df = self.get_watercut()
        hist_df['Comment'] = 'history_data'
        frame = np.column_stack((RF_predict, Swav_predict, Sw_predic, fw_predict))
        frame = pd.DataFrame(frame, columns=['R','Swav', 'Sw', 'fw_model'])
        frame['fw_hist'] = np.NAN
        frame['Comment'] = 'forecast'
        frame = pd.concat([hist_df, frame])
        frame = frame.query('fw_model<0.98')
        frame['OPT'] = self.N * frame['R']
        return frame

    def wct_fitting(self):
        """Подгонка параметров модели к историческим данным"""
        # Фильтруем данные, где R > 0 и wcth в допустимом диапазоне
        valid_mask = (self.R > 0) & (self.wcth >= 0) & (self.wcth <= 0.8)
        R_valid = self.R[valid_mask]
        wcth_valid = self.wcth[valid_mask]
        
        if len(R_valid) == 0:
            print("Нет валидных данных для подгонки")
            return None, None
        
        # Задаем начальные значения параметров
        initial_guess = [self.lam, 1.0, 1.0]  # lam, nw, no
        
        # Задаем границы параметров
        bounds = ([0.8, 0.1, 0.1], [1.5, 10.0, 10.0])  # более узкие границы для стабильности
        
        try:
            # Выполняем подгонку
            popt, pcov = curve_fit(
                self.watercut_from_wor, 
                R_valid, 
                wcth_valid, 
                p0=initial_guess,
                bounds=bounds,
                maxfev=5000,
                method='trf'  # метод, более устойчивый к ошибкам
            )
            
            # Обновляем параметры модели
            self.lam_fit, self.nw_fit, self.no_fit = popt
            print(f"Оптимальные параметры: lam={popt[0]:.4f}, nw={popt[1]:.4f}, no={popt[2]:.4f}")
            
            return popt, pcov
            
        except Exception as e:
            print(f"Ошибка при подгонке: {e}")
            print("Попробуйте изменить начальные значения или границы параметров")
            return None, None

    def plot_results(self, popt=None):
        """Визуализация результатов"""
        plt.figure(figsize=(12, 5))
        
        # Исторические данные
        plt.subplot(1, 2, 1)
        plt.plot(self.R, self.wcth, 'bo-', label='Исторические данные', markersize=4)
        
        # Если есть подобранные параметры, строим кривую
        if popt is not None:
            lam_fit, nw_fit, no_fit = popt
            fw_fitted = self.watercut_from_wor(self.R, lam_fit, nw_fit, no_fit)
            plt.plot(self.R, fw_fitted, 'r-', label='Подгонка модели', linewidth=2)
        
        plt.xlabel('КИН (R)')
        plt.ylabel('Обводненность')
        plt.title('Подгонка модели обводненности')
        plt.legend()
        plt.grid(True)
        
        # График остатков
        if popt is not None:
            plt.subplot(1, 2, 2)
            residuals = self.wcth - fw_fitted
            plt.plot(self.R, residuals, 'go-', markersize=4)
            plt.axhline(y=0, color='r', linestyle='--')
            plt.xlabel('КИН (R)')
            plt.ylabel('Остатки')
            plt.title('Остатки подгонки')
            plt.grid(True)
        
        plt.tight_layout()
        plt.show()   
    
    # %%
df = pd.read_csv('/home/albert/Документы/decliner/test_data/test_wor_func.csv')
field = WOR_forecaster(**{'Swi': 0.3, 
                              'Sor': 0.3,
                              'muo':2.47,
                              'muw':0.4,
                              'krw':0.2,
                              'kro':1,
                              'N': 18680*2,
                              'lam': 1.01})
    # df
field.set_hist_data(df)
# %%
df = field.wct_forecast()
# %%
n = field.limit_calc(field.nw_fit, field.no_fit, 0.98)

# field.R_lim
