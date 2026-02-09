import numpy as np
import pandas as pd


def filter_and_calculate_percentiles_by_date(
    df, wells=None, valid_statuses=["prod"], save_to_csv=True
):
    """
    Фильтрует данные по статусу и скважинам, группирует по дате и рассчитывает перцентили для каждой даты

    Args:
        df (pd.DataFrame): исходные данные с колонкой 'date'
        wells (list, optional): список скважин для фильтрации
        save_to_csv (bool): сохранять результаты в CSV файлы

    Returns:
        dict: словарь с перцентилями по датам {date: {column: {P10, P50, P90}}}
    """
    # Фильтрация по статусу
    filtered_df = df[df["status"].isin(valid_statuses)].copy()

    # Фильтрация по скважинам
    if wells is not None:
        filtered_df = filtered_df[filtered_df["well"].isin(wells)]

    # Группировка по дате и расчет перцентилей
    date_groups = filtered_df.groupby("date")
    percentiles_by_date = {}

    for date, group in date_groups:
        numeric_cols = group.select_dtypes(include=[np.number]).columns
        percentiles = {}

        for col in numeric_cols:
            if (
                not group[col].empty and group[col].count() > 0
            ):  # Проверка на наличие данных
                percentiles[col] = {
                    "P10": group[col].quantile(0.10),
                    "P50": group[col].quantile(0.50),
                    "P90": group[col].quantile(0.90),
                }

        percentiles_by_date[date] = percentiles

    # Сохранение в CSV если требуется
    if save_to_csv:
        save_grouped_percentiles_to_csv(percentiles_by_date)

    return percentiles_by_date


def save_grouped_percentiles_to_csv(percentiles_by_date):
    """
    Сохраняет перцентили по датам в отдельные CSV файлы

    Args:
        percentiles_by_date (dict): словарь с перцентилями по датам
    """
    # Создаем DataFrame для каждого перцентиля
    p10_records = []
    p50_records = []
    p90_records = []

    for date, columns in percentiles_by_date.items():
        p10_record = {"date": date}
        p50_record = {"date": date}
        p90_record = {"date": date}

        for col, values in columns.items():
            p10_record[col] = values["P10"]
            p50_record[col] = values["P50"]
            p90_record[col] = values["P90"]

        p10_records.append(p10_record)
        p50_records.append(p50_record)
        p90_records.append(p90_record)

    # Сохраняем в файлы
    pd.DataFrame(p10_records).to_csv("P10.csv", index=False)
    pd.DataFrame(p50_records).to_csv("P50.csv", index=False)
    pd.DataFrame(p90_records).to_csv("P90.csv", index=False)

