from typing import List, Any, Optional
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class WellNeighborFinder:
    """
    Класс для поиска соседних скважин в заданном радиусе.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        well_col: str = "well",
        x_col: str = "east",
        y_col: str = "north",
    ):
        """
        Инициализация класса для поиска соседей по координатам скважин.

        Аргументы:
            df (pd.DataFrame): DataFrame с данными по скважинам.
            well_col (str): Имя столбца с Номером скважины.
            x_col (str): Имя столбца с координатой X (например, 'east').
            y_col (str): Имя столбца с координатой Y (например, 'north').

        Исключения:
            ValueError: Если отсутствуют необходимые столбцы или DataFrame пустой.
        """
        self._validate_input_df(df, [well_col, x_col, y_col])

        self.df = df.copy(deep=True).reset_index(drop=True)
        self.well_col = well_col
        self.x_col = x_col
        self.y_col = y_col

        self._wells = self.df[well_col].values
        self._coords = self.df[[x_col, y_col]].values

    @staticmethod
    def _validate_input_df(df: pd.DataFrame, columns: List[str]) -> None:
        """
        Проверка наличия всех необходимых столбцов и непустоты DataFrame.

        Аргументы:
            df (pd.DataFrame): Исходный DataFrame.
            columns (List[str]): Список обязательных столбцов.

        Исключения:
            ValueError: Если DataFrame пустой или отсутствуют требуемые столбцы.
        """
        if df.empty:
            raise ValueError("Входной DataFrame пуст.")
        missing = set(columns) - set(df.columns)
        if missing:
            raise ValueError(f"В DataFrame отсутствуют необходимые столбцы: {missing}")

    def radius_neighbors(
        self, 
        target_well: Any, 
        radius: float = 1000.0,
        return_distance: bool = False
    ) -> List[Any]:
        """
        Находит скважины в заданном радиусе от целевой скважины.

        Аргументы:
            target_well (Any): Номер целевой скважины.
            radius (float): Радиус поиска, в тех же единицах, что и координаты.
            return_distance (bool): Если True, возвращает список кортежей (скважина, расстояние).

        Возвращает:
            List[Any] или List[Tuple[Any, float]]: Список соседних скважин (или кортежей "скважина, расстояние" при return_distance=True).

        Исключения:
            ValueError: Если целевая скважина не найдена.
        """
        idx = self._find_well_index(target_well)
        dists = np.linalg.norm(self._coords - self._coords[idx], axis=1)
        mask = (dists <= radius) & (self._wells != target_well)
        neighbors = self._wells[mask]
        if return_distance:
            return list(zip(neighbors, dists[mask]))
        return neighbors.tolist()
    
    def knn_neighbors(
        self,
        target_well: Any,
        k: int = 1,
        return_distance: bool = False
    ) -> List[Any]:
        """
        Находит k ближайших скважин к целевой скважине.

        Аргументы:
            target_well (Any): Идентификатор целевой скважины.
            k (int): Количество ближайших скважин для поиска (k >= 1).
            return_distance (bool): Если True, возвращает список кортежей (скважина, расстояние).

        Возвращает:
            List[Any] или List[Tuple[Any, float]]: Список k ближайших скважин (или кортежей "скважина, расстояние" при return_distance=True).

        Исключения:
            ValueError: Если целевая скважина не найдена или k слишком велико.
        """
        idx = self._find_well_index(target_well)
        dists = np.linalg.norm(self._coords - self._coords[idx], axis=1)
        mask = self._wells != target_well
        neighbor_indices = np.where(mask)[0]
        neighbor_dists = dists[neighbor_indices]

        if len(neighbor_indices) == 0:
            return []
        if k > len(neighbor_indices):
            logger.warning(f"Запрошено k={k} ближайших скважин, но найдено только {len(neighbor_indices)}.")
            k = len(neighbor_indices)

        # Получаем индексы k минимальных расстояний
        k_idx = np.argpartition(neighbor_dists, k - 1)[:k]
        sorted_idx = k_idx[np.argsort(neighbor_dists[k_idx])]

        nearest_wells = self._wells[neighbor_indices][sorted_idx]
        nearest_dists = neighbor_dists[sorted_idx]

        if return_distance:
            return list(zip(nearest_wells, nearest_dists))
        return nearest_wells.tolist()
    
    def _find_well_index(self, well: Any) -> int:
        """
        Возвращает индекс скважины в self._wells.

        Аргументы:
            well (Any): Номер скважины.

        Исключения:
            ValueError: Если скважина не найдена.
        """
        matches = np.where(self._wells == well)[0]
        if not matches.size:
            logger.error(f"Скважина '{well}' не найдена.")
            raise ValueError(f"Скважина '{well}' не найдена в столбце {self.well_col}.")
        return matches[0]


# Пример использования:
# df = pd.DataFrame({
#     'well': ['A', 'B', 'C', 'D'],
#     'east': [0, 100, 200, 300],
#     'north': [0, 0, 0, 0],
# })
# finder = WellNeighborFinder(df)
# print(finder.radius_neighbors('A', radius=150))  # ['B']
# print(finder.radius_neighbors('A', radius=250, return_distance=True))  # [('B', 100.0), ('C', 200.0)]
# print(finder.neighbors_by_k('A', k=2, return_distance=True))  # [('B', 100.0), ('C', 200.0)]
