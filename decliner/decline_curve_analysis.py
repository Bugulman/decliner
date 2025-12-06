import numpy as np
from scipy.optimize import curve_fit
from typing import Callable, Tuple, Optional, Any, Sequence


class DeclineCurveAnalysis:
    """
    Класс для расчёта и подбора кривых снижения добычи (DCA) на основе различных моделей.
    """

    @staticmethod
    def exponential_decline(t: np.ndarray, qi: float, Di: float) -> np.ndarray:
        """
        Экспоненциальная модель снижения дебита скважины.

        Аргументы:
            t: np.ndarray — Время эксплуатации с момента ввода скважины (дни, месяцы и т.д.).
            qi: float — Начальный дебит.
            Di: float — Начальная скорость снижения (константа).

        Возвращает:
            np.ndarray — Дебит скважины в моменты времени t.
        """
        return qi * np.exp(-Di * t)

    @staticmethod
    def hyperbolic_decline(t: np.ndarray, qi: float, b: float, Di: float) -> np.ndarray:
        """
        Гиперболическая модель снижения дебита скважины.

        Аргументы:
            t: np.ndarray — Время эксплуатации с момента ввода скважины (дни, месяцы и т.д.).
            qi: float — Начальный дебит.
            b: float — Показатель гиперболичности (0 < b < 2).
            Di: float — Начальная скорость снижения.

        Возвращает:
            np.ndarray — Дебит скважины в моменты времени t.
        """
        return qi / np.power((1 + b * Di * t), 1 / b)

    @staticmethod
    def harmonic_decline(t: np.ndarray, qi: float, Di: float) -> np.ndarray:
        """
        Гармоническая модель снижения дебита скважины.

        Аргументы:
            t: np.ndarray — Время эксплуатации с момента ввода скважины.
            qi: float — Начальный дебит.
            Di: float — Начальная скорость снижения.

        Возвращает:
            np.ndarray — Дебит скважины в моменты времени t.
        """
        return qi / (1 + Di * t)

    @staticmethod
    def hyp2exp(t: np.ndarray, qi: float, Di: float, b: float, beta: float) -> np.ndarray:
        """
        Модель перехода от гиперболического к экспоненциальному снижению.

        Аргументы:
            t: np.ndarray — Время эксплуатации с момента ввода скважины.
            qi: float — Начальный дебит.
            Di: float — Начальная скорость снижения.
            b: float — Показатель гиперболичности (0 < b < 2).
            beta: float — Параметр перехода (0 < beta < 1).

        Возвращает:
            np.ndarray — Дебит скважины в моменты времени t.
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
        Подбор оптимальных параметров для заданной модели кривой снижения методом наименьших квадратов.

        Аргументы:
            func: Callable — Модельная функция, для которой проводится подбор параметров.
            time: Sequence[float] — Массив времени (в выбранных единицах, например, месяца).
            production: Sequence[float] — Массив наблюдаемых дебитов.
            p0: Optional[Sequence[Any]] — Начальные приближения для параметров (по умолчанию None).
            bounds: Tuple[Any, Any] — Ограничения на параметры (по умолчанию нет ограничений).

        Возвращает:
            Tuple[np.ndarray, np.ndarray]: 
                - Массив оптимальных параметров,
                - Ковариационная матрица оценки параметров.
        """
        time = np.asarray(time)
        production = np.asarray(production)
        try:
            popt, pcov = curve_fit(func, time, production, maxfev=10000, p0=p0, bounds=bounds)
        except RuntimeError:
            popt, pcov = curve_fit(func, time[:-2], production[:-2], maxfev=10000, p0=p0, bounds=bounds)
        return popt, pcov
