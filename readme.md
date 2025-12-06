# Описание модуля

Модуль для работы с гидродинамическими моделями в ПО **tNavigator**.

## Установка

```bash
pip install oilyreports-1.1.tar.gz
```

## Требуемые пакеты

```python
import pandas as pd
import os
import datetime
import getpass
```

## Связь с классами tNavigator

```python
keyword = {
    'grou': get_all_groups(),
    'wells': get_all_wells(),
    'mod': get_all_models(),
    'step': get_all_timesteps()
}
```

## Список функций

| Функция                     | Описание                                                                  | Параметры                                                                                                                                                                                                                                                                                                                |
| --------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `create_report_dir`         | Создает папку `result` и устанавливает её по умолчанию при записи файлов. | `path: str` – путь, где будет создана папка.                                                                                                                                                                                                                                                                             |
| `dataframe_creater`         | Преобразует формат данных из tNavigator в `pandas.DataFrame`.             | `*args`: список колонок для вывода.<br>`dimens`: `well` или `group` – тип данных.<br>`start`: дата начала формирования фрейма.                                                                                                                                                                                           |
| `df_from_histtab`           | Создаёт `DataFrame` с данными из таблицы истории модели.                  | `paramert_list`: список параметров для выгрузки (получить через `get_production_types`).<br>`keyword`: словарь с параметрами:<br>`'wells'`: `get_well_filter_by_name(name='14').get_wells()` – список скважин.<br>`'mod'`: `get_all_wells_production_tables()[0]` – таблица истории.<br>`'step'`: `get_all_timesteps()`. |
| `interpolate_press_by_sipy` | Интерполирует и сглаживает давление, используя SciPy.                     | Требуются колонки `BHPH` (bottom‑hole pressure) и `THPH` (top‑hole pressure).<br>Возвращает `DataFrame` с сглаженными значениями давления.                                                                                                                                                                               |
| `interpolate_prod_by_sipy`  | Сглаживает добычу, используя SciPy.                                       | Требуются колонки `QLIQ` (жидкостный поток) и `WCT` (пропуск воды).<br>Возвращает `DataFrame` со сглаженными данными добычи.                                                                                                                                                                                             |
| `adapt_report`              | Выдаёт фрейм данных с основными показателями адаптации модели.            | `model_id`: идентификатор модели.                                                                                                                                                                                                                                                                                        |

## Пример использования

```python
from decliner import create_report_dir, dataframe_creater

# Создание каталога отчётов
create_report_dir('/path/to/reports')

# Получение датафрейма по скважинам
df = dataframe_creater(
    'BHPH', 'THPH', 'QLIQ',
    dimens='well',
    start='2020-01-01'
)
```

---

Дополнительную информацию и примеры можно найти в репозитории GitHub.
