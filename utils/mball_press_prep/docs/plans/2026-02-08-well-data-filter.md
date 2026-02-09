# Функция фильтрации данных по скважинам и расчета перцентилей Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Создать функцию для фильтрации данных по скважинам и расчета перцентилей P10, P50, P90

**Architecture:** Простая функция pandas с фильтрацией по статусу и скважинам, расчетом перцентилей и сохранением в CSV файлы

**Tech Stack:** pandas, numpy

---

### Task 1: Создание основной функции фильтрации

**Files:**
- Create: `well_data_filter.py`

**Step 1: Write the failing test**

```python
import pandas as pd
import pytest
from well_data_filter import filter_and_calculate_percentiles

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
```

**Step 2: Run test to verify it fails**

Run: `pytest test_well_data_filter.py -v`
Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
import pandas as pd
import numpy as np

def filter_and_calculate_percentiles(df, wells=None):
    """
    Фильтрует данные по статусу и скважинам, рассчитывает перцентили
    
    Args:
        df (pd.DataFrame): исходные данные
        wells (list, optional): список скважин для фильтрации
    
    Returns:
        dict: словарь с перцентилями P10, P50, P90
    """
    # Фильтрация по статусу
    valid_statuses = ['prod', 'not work', 'inj']
    filtered_df = df[df['status'].isin(valid_statuses)].copy()
    
    # Фильтрация по скважинам
    if wells is not None:
        filtered_df = filtered_df[filtered_df['well'].isin(wells)]
    
    # Расчет перцентилей для числовых колонок
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    percentiles = {}
    
    for col in numeric_cols:
        percentiles[col] = {
            'P10': filtered_df[col].quantile(0.10),
            'P50': filtered_df[col].quantile(0.50),
            'P90': filtered_df[col].quantile(0.90)
        }
    
    return percentiles
```

**Step 4: Run test to verify it passes**

Run: `pytest test_well_data_filter.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add well_data_filter.py test_well_data_filter.py
git commit -m "feat: add basic filter and percentile calculation function"
```

### Task 2: Добавление сохранения результатов в CSV файлы

**Files:**
- Modify: `well_data_filter.py`

**Step 1: Write the failing test**

```python
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
    import os
    assert os.path.exists('P10.csv')
    assert os.path.exists('P50.csv')
    assert os.path.exists('P90.csv')
    
    # Очистка
    os.remove('P10.csv')
    os.remove('P50.csv')
    os.remove('P90.csv')
```

**Step 2: Run test to verify it fails**

Run: `pytest test_well_data_filter.py::test_save_percentiles_to_csv -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def save_percentiles_to_csv(percentiles):
    """
    Сохраняет перцентили в отдельные CSV файлы
    
    Args:
        percentiles (dict): словарь с перцентилями
    """
    # Создаем DataFrame для каждого перцентиля
    p10_data = {}
    p50_data = {}
    p90_data = {}
    
    for col, values in percentiles.items():
        p10_data[col] = values['P10']
        p50_data[col] = values['P50']
        p90_data[col] = values['P90']
    
    # Сохраняем в файлы
    pd.DataFrame([p10_data]).to_csv('P10.csv', index=False)
    pd.DataFrame([p50_data]).to_csv('P50.csv', index=False)
    pd.DataFrame([p90_data]).to_csv('P90.csv', index=False)
```

**Step 4: Run test to verify it passes**

Run: `pytest test_well_data_filter.py::test_save_percentiles_to_csv -v`
Expected: PASS

**Step 5: Commit**

```bash
git add well_data_filter.py test_well_data_filter.py
git commit -m "feat: add CSV export functionality for percentiles"
```

### Task 3: Обновление основной функции для автоматического сохранения

**Files:**
- Modify: `well_data_filter.py`

**Step 1: Write the failing test**

```python
def test_filter_and_calculate_percentiles_with_save():
    test_data = pd.DataFrame({
        'status': ['prod', 'prod'],
        'well': ['14312', '14314'],
        'QOIL': [16.27, 1.34],
        'QWAT': [248.21, 33.23]
    })
    
    result = filter_and_calculate_percentiles(test_data, save_to_csv=True)
    
    # Проверяем наличие файлов
    import os
    assert os.path.exists('P10.csv')
    assert os.path.exists('P50.csv')
    assert os.path.exists('P90.csv')
    
    # Очистка
    os.remove('P10.csv')
    os.remove('P50.csv')
    os.remove('P90.csv')
```

**Step 2: Run test to verify it fails**

Run: `pytest test_well_data_filter.py::test_filter_and_calculate_percentiles_with_save -v`
Expected: FAIL with "unexpected keyword argument"

**Step 3: Write minimal implementation**

```python
def filter_and_calculate_percentiles(df, wells=None, save_to_csv=False):
    """
    Фильтрует данные по статусу и скважинам, рассчитывает перцентили
    
    Args:
        df (pd.DataFrame): исходные данные
        wells (list, optional): список скважин для фильтрации
        save_to_csv (bool): сохранять результаты в CSV файлы
    
    Returns:
        dict: словарь с перцентилями P10, P50, P90
    """
    # Фильтрация по статусу
    valid_statuses = ['prod', 'not work', 'inj']
    filtered_df = df[df['status'].isin(valid_statuses)].copy()
    
    # Фильтрация по скважинам
    if wells is not None:
        filtered_df = filtered_df[filtered_df['well'].isin(wells)]
    
    # Расчет перцентилей для числовых колонок
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    percentiles = {}
    
    for col in numeric_cols:
        percentiles[col] = {
            'P10': filtered_df[col].quantile(0.10),
            'P50': filtered_df[col].quantile(0.50),
            'P90': filtered_df[col].quantile(0.90)
        }
    
    # Сохранение в CSV если требуется
    if save_to_csv:
        save_percentiles_to_csv(percentiles)
    
    return percentiles
```

**Step 4: Run test to verify it passes**

Run: `pytest test_well_data_filter.py::test_filter_and_calculate_percentiles_with_save -v`
Expected: PASS

**Step 5: Commit**

```bash
git add well_data_filter.py test_well_data_filter.py
git commit -m "feat: add automatic CSV saving option"
```

### Task 4: Создание примера использования

**Files:**
- Create: `example_usage.py`

**Step 1: Write example usage**

```python
import pandas as pd
from well_data_filter import filter_and_calculate_percentiles

# Пример использования функции
def main():
    # Загрузка данных (заменить на реальный путь к файлу)
    # df = pd.read_csv('your_data.csv')
    
    # Создание тестовых данных для примера
    df = pd.DataFrame({
        'status': ['prod', 'prod', 'not work', 'inj', 'other', 'prod'],
        'well': ['14312', '14314', '14312', '14316', '14312', '14314'],
        'QOIL': [16.27, 1.34, 12.49, 2.05, 3.69, 18.43],
        'QWAT': [248.21, 33.23, 244.02, 0.52, 62.43, 123.46],
        'BHPH': [102.87, 128.38, 73.64, 60.30, 80.11, 48.33],
        'THPH': [156.18, 157.57, 147.90, 97.77, 135.49, 149.96]
    })
    
    # Базовое использование - фильтрация по статусу
    result = filter_and_calculate_percentiles(df, save_to_csv=True)
    print("Рассчитанные перцентили:")
    for col, values in result.items():
        print(f"{col}: P10={values['P10']:.2f}, P50={values['P50']:.2f}, P90={values['P90']:.2f}")
    
    # Фильтрация по конкретным скважинам
    specific_wells = ['14312', '14314']
    result_wells = filter_and_calculate_percentiles(df, wells=specific_wells, save_to_csv=True)
    print(f"\nПерцентили для скважин {specific_wells}:")
    for col, values in result_wells.items():
        print(f"{col}: P10={values['P10']:.2f}, P50={values['P50']:.2f}, P90={values['P90']:.2f}")

if __name__ == "__main__":
    main()
```

**Step 2: Run example**

Run: `python example_usage.py`
Expected: Успешное выполнение с выводом перцентилей и созданием файлов P10.csv, P50.csv, P90.csv

**Step 3: Commit**

```bash
git add example_usage.py
git commit -m "docs: add example usage script"
```

### Task 5: Финальное тестирование и документация

**Files:**
- Create: `README.md`

**Step 1: Write documentation**

```markdown
# Well Data Filter and Percentile Calculator

Простая функция для фильтрации данных по скважинам и расчета перцентилей.

## Функциональность

- Фильтрация данных по статусу (prod, not work, inj)
- Опциональная фильтрация по списку скважин
- Расчет перцентилей P10, P50, P90 для всех числовых колонок
- Сохранение результатов в CSV файлы

## Использование

```python
import pandas as pd
from well_data_filter import filter_and_calculate_percentiles

# Загрузка данных
df = pd.read_csv('your_data.csv')

# Базовая фильтрация и расчет
result = filter_and_calculate_percentiles(df, save_to_csv=True)

# Фильтрация по конкретным скважинам
result = filter_and_calculate_percentiles(df, wells=['14312', '14314'], save_to_csv=True)
```

## Результаты

Создаются три файла:
- `P10.csv` - 10-й перцентиль
- `P50.csv` - медиана (50-й перцентиль)  
- `P90.csv` - 90-й перцентиль
```

**Step 2: Run final tests**

Run: `pytest test_well_data_filter.py -v`
Expected: Все тесты проходят

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add README documentation"
```

---

**Plan complete and saved to `docs/plans/2026-02-08-well-data-filter.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**