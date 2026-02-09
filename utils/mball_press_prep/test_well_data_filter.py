import pandas as pd
import pytest
import os
from well_data_filter import filter_and_calculate_percentiles, save_percentiles_to_csv

def test_filter_and_calculate_percentiles():
    # Создаем тестовые данные
    test_data = pd.DataFrame({
        'status': ['prod', 'prod', 'not work', 'inj', 'other'],
        'well': ['14312', '14314', '14312', '14316', '14312'],
        'QOIL': [16.27, 1.34, 12.49, 2.05, 3.69],
        'QWAT': [248.21, 33.23, 244.02, 0.52, 62.43],
        'BHPH': [102.87, 128.38, 73.64, 60.30, 80.11]
    })
    
    result = filter_and_calculate_percentiles(test_data)
    assert result is not None
    assert len(result) == 3  # P10, P50, P90

def test_save_percentiles_to_csv():
    test_data = pd.DataFrame({
        'status': ['prod', 'prod'],
        'well': ['14312', '14314'],
        'QOIL': [16.27, 1.34],
        'QWAT': [248.21, 33.23]
    })
    
    result = filter_and_calculate_percentiles(test_data)
    save_percentiles_to_csv(result)
    
    # Проверяем наличие файлов
    assert os.path.exists('P10.csv')
    assert os.path.exists('P50.csv')
    assert os.path.exists('P90.csv')
    
    # Очистка
    os.remove('P10.csv')
    os.remove('P50.csv')
    os.remove('P90.csv')
