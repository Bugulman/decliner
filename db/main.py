from datetime import datetime, timedelta
from crud_operations import WellOperations
from sqlalchemy.orm import Session


def main():
    # Инициализация
    ops = WellOperations()
    session = ops.db.get_session()

    try:
        # 1. Добавление скважины
        well_data = {
            "well_name": "Prod__1",
            "field": "Ромашкинское",
            "area": "Участок 1А",
            "well_type": "Добывающая",
            "status": "В работе",
            "coordinates_x": 55.123456,
            "coordinates_y": 51.789012,
            "completion_date": datetime(2020, 1, 15),
        }

        well = ops.add_well(session, well_data)
        print(f"Добавлена скважина: {well.well_name}")

        # 2. Добавление геологических параметров
        geo_params = {
            "porosity": 0.15,
            "permeability": 120.5,
            "net_pay": 12.3,
            "water_saturation": 0.25,
            "formation_pressure": 240.8,
            "temperature": 85.0,
        }

        ops.add_geological_parameters(session, well.id, geo_params)

        # 3. Добавление данных по добыче
        production_records = []
        start_date = datetime(2023, 1, 1)

        for i in range(30):  # 30 дней данных
            record = {
                "date": start_date + timedelta(days=i),
                "oil_rate": 100.0 - i * 2,  # Примерные данные
                "gas_rate": 50.0 - i * 0.5,
                "water_rate": 20.0 + i * 0.3,
                "water_cut": 0.2 + i * 0.01,
                "bottomhole_pressure": 200.0 - i * 1.5,
            }
            production_records.append(record)

        ops.add_production_data(session, well.id, production_records)

        # 4. Запросы
        # Получение всех данных по скважине
        well_data = ops.get_well_with_all_data(session, "Prod__1")
        print(f"Геологические параметры: {well_data['geological_params']}")

        # Получение добычи за период
        production = ops.get_production_for_period(
            session, "Prod__1", datetime(2023, 1, 1), datetime(2023, 1, 10)
        )
        print(f"Количество записей за период: {len(production)}")

        # Месячная добыча
        monthly = ops.calculate_monthly_production(session, "Prod__1", 2023, 1)
        print(f"Месячная добыча нефти: {monthly.total_oil}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
