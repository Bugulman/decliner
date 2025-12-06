from dataclasses import dataclass
import numpy as np


@dataclass
class ProductionParameters:
    """Класс для хранения параметров добычи"""
    liquid_rate: float          # дебит жидкости
    water_cut: float            # обводненность (%)
    reservoir_pressure: float   # пластовое давление
    bottomhole_pressure: float  # забойное давление
    oil_density: float          # плотность нефти


class FactorCalculator:
    """
    Класс для расчета различных отклонений в показателях добычи.
    """
    
    def __init__(self, current: ProductionParameters, previous: ProductionParameters, decimals: int = 3):
        """
        Инициализация калькулятора.
        
        :param current: текущие параметры добычи
        :param previous: предыдущие параметры добычи (опционально)
        """
        self.current = current
        self.previous = previous
        self.decimals = decimals
        
    def oil_deviation(self) -> float:
        """Рассчитывает общее отклонение по нефти"""
        self._validate_previous_params()
        return self._round_result(
            (self.current.liquid_rate - self.previous.liquid_rate) * self.current.oil_density * self._oil_fraction() -
            self.previous.liquid_rate * self.current.oil_density * self._water_cut_change()
        )
     
    def liquid_deviation(self) -> float:
        """Рассчитывает отклонение по жидкости"""
        self._validate_previous_params()
        return self._round_result(
            (self.current.liquid_rate - self.previous.liquid_rate) * 
            self.current.oil_density * 
            self._oil_fraction()
        )
    
    def water_cut_deviation(self) -> float:
        """Рассчитывает отклонение по обводненности"""
        self._validate_previous_params()
        return self._round_result(
            -self.previous.liquid_rate * 
            self.current.oil_density * 
            self._water_cut_change()
        )
    
    def reservoir_pressure_deviation(self) -> float:
        """Рассчитывает отклонение по пластовому давлению"""
        self._validate_previous_params()
        pressure_diff = self.current.reservoir_pressure - self.current.bottomhole_pressure
        self._check_pressure_diff(pressure_diff)

        return self._round_result(
            (self.current.liquid_rate / pressure_diff) *
            (self.current.reservoir_pressure - self.previous.reservoir_pressure) *
            self.current.oil_density *
            self._oil_fraction()
        )
    
    def bottomhole_pressure_deviation(self) -> float:
        """Рассчитывает отклонение по забойному давлению"""
        self._validate_previous_params()
        pressure_diff = self.current.reservoir_pressure - self.current.bottomhole_pressure
        self._check_pressure_diff(pressure_diff)

        return self._round_result(
            -(self.current.liquid_rate / pressure_diff) *
            (self.current.bottomhole_pressure - self.previous.bottomhole_pressure) *
            self.current.oil_density *
            self._oil_fraction()
        )
    
    def productivity_index_deviation(self) -> float:
        """Рассчитывает отклонение по коэффициенту продуктивности"""
        self._validate_previous_params()
        current_pressure_diff = self.current.reservoir_pressure - self.current.bottomhole_pressure
        previous_pressure_diff = self.previous.reservoir_pressure - self.previous.bottomhole_pressure

        self._check_pressure_diff(current_pressure_diff)
        self._check_pressure_diff(previous_pressure_diff)

        return self._round_result(
            previous_pressure_diff *
            ((self.current.liquid_rate / current_pressure_diff) - 
             (self.previous.liquid_rate / previous_pressure_diff)) *
            self.current.oil_density *
            self._oil_fraction()
        )
    
    def _oil_fraction(self) -> float:
        """Рассчитывает долю нефти в потоке (1 - wcut/100)"""
        return (1 - self.current.water_cut / 100)
    
    def _water_cut_change(self) -> float:
        """Рассчитывает изменение обводненности"""
        return (self.current.water_cut - self.previous.water_cut) / 100
    
    def _check_pressure_diff(self, diff: float):
        """Проверяет корректность давлений"""
        if np.isclose(diff, 0):
            raise ValueError("Разница между пластовым и забойным давлением не может быть нулевой")

    def _validate_previous_params(self) -> None:
        """Проверяет наличие предыдущих параметров"""
        if self.previous is None:
            raise ValueError("Для расчета отклонений требуются предыдущие параметры")
    
    def _round_result(self, value: float) -> float:
        """Округляет результат вычислений"""
        return round(value, self.decimals)


# Пример использования
# current = ProductionParameters(
#     liquid_rate=220,
#     water_cut=94.6,
#     reservoir_pressure=149,
#     bottomhole_pressure=111,
#     oil_density=0.848
# )

# previous = ProductionParameters(
#     liquid_rate=210,
#     water_cut=95,
#     reservoir_pressure=137,
#     bottomhole_pressure=108,
#     oil_density=0.848
# )

# calculator = FactorCalculator(current, previous)
# oil_dev = calculator.oil_deviation()
# liq_dev = calculator.liquid_deviation()
# wcut_dev = calculator.water_cut_deviation()
# wbp_dev = calculator.reservoir_pressure_deviation()
# bhp_dev = calculator.bottomhole_pressure_deviation()
# pi_dev = calculator.productivity_index_deviation()
# print(f"Отклонение по нефти: {oil_dev}")
# print(f"Отклонение по жидкости: {liq_dev}")
# print(f"Отклонение по обводненности: {wcut_dev}")
# print(f"Отклонение по Рпл: {wbp_dev}")
# print(f"Отклонение по Рзаю: {bhp_dev}")
# print(f"Отклонение по Кпрод: {pi_dev}")