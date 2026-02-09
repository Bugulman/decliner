"""
Enhanced Decline Curve Analysis Module

Consolidated module combining the best functionality from:
- decliner/decline_curve_analysis.py (structured class-based approach)
- decliner/dca_per_well.py (additional utilities and bootstrapping)
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import Callable, Tuple, Optional, Any, Sequence, Union
import matplotlib.pyplot as plt
import pandas as pd


class DeclineCurveAnalysis:
    """
    Comprehensive class for decline curve analysis (DCA) with multiple models and utilities.
    """

    @staticmethod
    def exponential_decline(t: np.ndarray, qi: float, Di: float) -> np.ndarray:
        """
        Exponential decline model.
        
        Arguments:
            t: np.ndarray — Time from well start (days, months, etc.)
            qi: float — Initial rate
            Di: float — Initial decline rate (constant)
            
        Returns:
            np.ndarray — Well rate at time t
        """
        return qi * np.exp(-Di * t)

    @staticmethod
    def hyperbolic_decline(t: np.ndarray, qi: float, b: float, Di: float) -> np.ndarray:
        """
        Hyperbolic decline model.
        
        Arguments:
            t: np.ndarray — Time from well start
            qi: float — Initial rate
            b: float — Hyperbolic exponent (0 < b < 2)
            Di: float — Initial decline rate
            
        Returns:
            np.ndarray — Well rate at time t
        """
        return qi / np.power((1 + b * Di * t), 1 / b)

    @staticmethod
    def harmonic_decline(t: np.ndarray, qi: float, Di: float) -> np.ndarray:
        """
        Harmonic decline model.
        
        Arguments:
            t: np.ndarray — Time from well start
            qi: float — Initial rate
            Di: float — Initial decline rate
            
        Returns:
            np.ndarray — Well rate at time t
        """
        return qi / (1 + Di * t)

    @staticmethod
    def hyp2exp(t: np.ndarray, qi: float, Di: float, b: float, beta: float) -> np.ndarray:
        """
        Hyperbolic to exponential transition model.
        
        Arguments:
            t: np.ndarray — Time from well start
            qi: float — Initial rate
            Di: float — Initial decline rate
            b: float — Hyperbolic exponent (0 < b < 2)
            beta: float — Transition parameter (0 < beta < 1)
            
        Returns:
            np.ndarray — Well rate at time t
        """
        numerator = (1 - beta) ** b * np.exp(-Di * t)
        denominator = (1 - beta * np.exp(-Di * t)) ** b
        return qi * numerator / denominator

    @staticmethod
    def fit_function(
        func: Callable[..., np.ndarray],
        time: Sequence[float],
        production: Sequence[float],
        p0: Optional[Sequence[Any]] = None,
        bounds: Tuple[Any, Any] = (-np.inf, np.inf)
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit optimal parameters for decline curve model using least squares.
        
        Arguments:
            func: Callable — Model function to fit
            time: Sequence[float] — Time array
            production: Sequence[float] — Observed rates
            p0: Optional[Sequence[Any]] — Initial parameter guesses
            bounds: Tuple[Any, Any] — Parameter bounds
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Optimal parameters and covariance matrix
        """
        time = np.asarray(time)
        production = np.asarray(production)
        try:
            popt, pcov = curve_fit(func, time, production, maxfev=10000, p0=p0, bounds=bounds)
        except RuntimeError:
            popt, pcov = curve_fit(func, time[:-2], production[:-2], maxfev=10000, p0=p0, bounds=bounds)
        return popt, pcov

    @staticmethod
    def arps_fit(t: Union[np.ndarray, Sequence], q: Union[np.ndarray, Sequence], 
                 plot: bool = False) -> Tuple[float, float, float, float]:
        """
        Arps Decline Curve Analysis using Non-Linear Curve-Fitting
        
        Input:
        t = time array (in numpy datetime64 or similar)
        q = production rate array
        plot = bool, whether to create plot
        
        Output:
        qi = initial production rate
        di = initial decline rate
        b = decline exponent
        RMSE = root mean square error
        """
        # Convert to numpy arrays
        t = np.asarray(t)
        q = np.asarray(q)
        
        def hyperbolic(t, qi, di, b):
            return qi / (np.abs((1 + b * di * t))**(1/b))
        
        def rmse(y, yfit):
            N = len(y)
            return np.sqrt(np.sum((y-yfit)**2) / N)

        # Handle datetime conversion
        if t.dtype.kind in ['M', 'm']:  # datetime64 or timedelta64
            import datetime
            timedelta = [j-i for i, j in zip(t[:-1], t[1:])]
            timedelta = np.array(timedelta)
            timedelta = timedelta / datetime.timedelta(days=1)
            t = np.cumsum(timedelta)
            t = np.append(0, t)
        t = t.astype(float)

        # Normalize the time and rate data
        t_normalized = t / max(t)
        q_normalized = q / max(q)  

        # Fitting data with hyperbolic function
        popt, pcov = curve_fit(hyperbolic, t_normalized, q_normalized)
        qi, di, b = popt

        # RMSE is calculated on the normalized variables
        qfit_normalized = hyperbolic(t_normalized, qi, di, b)
        RMSE = rmse(q_normalized, qfit_normalized)

        # De-normalize qi and di
        qi = qi * max(q)
        di = di / max(t)

        if plot:
            # Print all parameters and RMSE
            print('Initial production rate (qi)  : {:.5f} VOL/D'.format(qi))
            print('Initial decline rate (di)     : {:.5f} VOL/D'.format(di))
            print('Decline coefficient (b)       : {:.5f}'.format(b))
            print('RMSE of regression            : {:.5f}'.format(RMSE))  

            # Produce the hyperbolic curve (fitted)
            tfit = np.linspace(min(t), max(t), 100)
            qfit = hyperbolic(tfit, qi, di, b)

            # Plot data and hyperbolic curve
            plt.figure(figsize=(10,7))
            plt.step(t, q, color='blue', label="Data")
            plt.plot(tfit, qfit, color='red', label="Hyperbolic Curve")
            plt.title('Decline Curve Analysis', size=20, pad=15)
            plt.xlabel('Days')
            plt.ylabel('Rate (VOL/D)')
            plt.xlim(min(t), max(t))
            plt.ylim(ymin=0)
            plt.legend()
            plt.grid()
            plt.show()

        return qi, di, b, RMSE

    @staticmethod
    def arps_bootstrap(t: Union[np.ndarray, Sequence], q: Union[np.ndarray, Sequence], 
                      size: int = 1, plot: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Bootstrapping of Decline Curves for uncertainty analysis
        
        Input:
        t = time array
        q = production rate array
        size = number of bootstrap replicates
        plot = whether to create plot
        
        Output:
        ci95_qi = 95% confidence interval for initial production rate
        ci95_di = 95% confidence interval for initial decline rate
        ci95_b = 95% confidence interval for decline exponent
        """
        def rmse(y, yfit):
            N = len(y)
            return np.sqrt(np.sum((y-yfit)**2) / N)

        # Convert to numpy arrays
        t = np.asarray(t)
        q = np.asarray(q)
        
        # Handle datetime conversion
        if t.dtype.kind in ['M', 'm']:  # datetime64 or timedelta64
            import datetime
            timedelta = [j-i for i, j in zip(t[:-1], t[1:])]
            timedelta = np.array(timedelta)
            timedelta = timedelta / datetime.timedelta(days=1)
            t = np.cumsum(timedelta)
            t = np.append(0, t)
        t = t.astype(float)

        # Normalize the time and rate data
        t_normalized = t / max(t)
        q_normalized = q / max(q)      

        # Set up array of indices to sample from
        inds = np.arange(0, len(t_normalized))

        # Initialize replicates for qi, di, b
        bs_qi_reps = np.empty(size)
        bs_di_reps = np.empty(size)
        bs_b_reps = np.empty(size)   

        if plot:
            plt.figure(figsize=(10,7)) 

        # Generate replicates
        for i in range(size):
            bs_inds = np.random.choice(inds, size=len(inds))
            bs_x, bs_y = t_normalized[bs_inds], q_normalized[bs_inds]
            popt, pcov = curve_fit(DeclineCurveAnalysis.hyperbolic_decline, bs_x, bs_y)

            # qi, di, and b replicates
            bs_qi_reps[i], bs_di_reps[i], bs_b_reps[i] = popt

            # De-normalize replicates
            bs_qi_reps[i] = bs_qi_reps[i] * max(q)
            bs_di_reps[i] = bs_di_reps[i] / max(t)
        
            if plot:
                # Produce hyperbolic curve (fitted)
                tfit = np.linspace(min(t), max(t), 100)
                qfit_reps = DeclineCurveAnalysis.hyperbolic_decline(tfit, bs_qi_reps[i], bs_b_reps[i], bs_di_reps[i])
                plt.plot(tfit, qfit_reps, color='orange', alpha=0.3)

        # Calculate 95% CI
        ci95_qi = np.percentile(bs_qi_reps, [2.5, 97.5])
        ci95_di = np.percentile(bs_di_reps, [2.5, 97.5])
        ci95_b = np.percentile(bs_b_reps, [2.5, 97.5])

        print("95% CI of initial production rate (qi) : {:.5f} to {:.5f} VOL/D".format(*ci95_qi))
        print("95% CI of initial decline rate (di)    : {:.5f} to {:.5f} VOL/D".format(*ci95_di))
        print("95% CI of decline exponent (b)         : {:.5f} to {:.5f}".format(*ci95_b))

        if plot:
            # The exact DCA
            qi, di, b, RMSE = DeclineCurveAnalysis.arps_fit(t, q)
            tfit = np.linspace(min(t), max(t), 100)
            qfit = DeclineCurveAnalysis.hyperbolic_decline(tfit, qi, b, di)    
            
            plt.plot(tfit, qfit_reps, color='orange', alpha=0.3, label="Replicates")
            plt.plot(tfit, qfit, color="red", label="Hyperbolic Curve")
            plt.step(t, q, color='blue', label="Data")
            plt.title('Decline Curve Analysis with Bootstrap', size=20, pad=15)
            plt.xlabel('Days')
            plt.ylabel('Rate (VOL/D)')
            plt.xlim(min(t), max(t))
            plt.ylim(0, max(q))
            plt.legend()
            plt.grid()
            plt.show()

        return ci95_qi, ci95_di, ci95_b

    @staticmethod
    def remove_outliers(df: pd.DataFrame, column_name: str, window: int, 
                       number_of_stdevs_away_from_mean: float, 
                       trim: bool = False) -> pd.DataFrame:
        """
        Remove outliers from production data and optionally trim initial buildup
        
        INPUT:
        df: Production dataframe
        column_name: Column name of production rate
        window: Rolling average window
        number_of_stdevs_away_from_mean: Distance from standard dev. where outliers will be removed
        trim: Option to trim initial buildup (because buildup is an outlier). Default is False.
        
        OUTPUT:
        df: New dataframe where outliers have been removed 
        """
        df_copy = df.copy()
        
        df_copy[column_name+'_rol_Av'] = df_copy[column_name].rolling(window=window, center=True).mean()
        df_copy[column_name+'_rol_Std'] = df_copy[column_name].rolling(window=window, center=True).std()

        # Detect anomalies by determining how far away from mean (in terms of standard deviation)
        df_copy[column_name+'_is_Outlier'] = (
            abs(df_copy[column_name] - df_copy[column_name+'_rol_Av']) > 
            (number_of_stdevs_away_from_mean * df_copy[column_name+'_rol_Std'])
        )
        
        # outlier and not-outlier will be recorded in '_is_Outlier'
        # column as 'True' and 'False'. Now, outlier is removed, so column that
        # contains 'True' values are masked out
        result = df_copy.drop(df_copy[df_copy[column_name+'_is_Outlier'] == True].index).reset_index(drop=True)

        # Remove rows where "_rol_Av" has NaNs
        result = result[result[column_name+'_rol_Av'].notna()]  

        if trim:
            # Trim initial buildup
            maxi = result[column_name+'_rol_Av'].max()
            maxi_index = (result[result[column_name+'_rol_Av']==maxi].index.values)[0]
            result = result.iloc[maxi_index:, :].reset_index(drop=True)

        return result

    @staticmethod
    def convert_date_to_days(t: Union[np.ndarray, Sequence]) -> np.ndarray:
        """
        Convert datetime array to days
        
        INPUT:
        t: datetime array
        
        OUTPUT:
        t: days array
        """
        # Convert to numpy if not already
        t = np.asarray(t)
        
        # Handle datetime conversion
        if t.dtype.kind in ['M', 'm']:  # datetime64 or timedelta64
            import datetime
            timedelta = [j-i for i, j in zip(t[:-1], t[1:])]
            timedelta = np.array(timedelta)
            timedelta = timedelta / datetime.timedelta(days=1)
            t = np.cumsum(timedelta)
            t = np.append(0, t)
        
        return t.astype(float)