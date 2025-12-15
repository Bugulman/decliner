from datetime import datetime
from sqlalchemy.orm import Session
from models import Well, GeologicalParameters, ProductionData
from database import DatabaseManager


class WellOperations:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.create_tables()

    def add_well(self, session: Session, well_data: dict):
        """Добавление новой скважины"""
        well = Well(**well_data)
        session.add(well)
        session.commit()
        return well

    def add_geological_parameters(self, session: Session, well_id: int, params: dict):
        """Добавление геологических параметров"""
        params["well_id"] = well_id
        geo_params = GeologicalParameters(**params)
        session.add(geo_params)
        session.commit()
        return geo_params

    def add_production_data(
        self, session: Session, well_id: int, production_records: list
    ):
        """Добавление данных по добыче"""
        for record in production_records:
            record["well_id"] = well_id
            prod_data = ProductionData(**record)
            session.add(prod_data)
        session.commit()

    def get_well_with_all_data(self, session: Session, well_name: str):
        """Получение всех данных по скважине"""
        well = session.query(Well).filter(Well.well_name == well_name).first()
        if well:
            return {
                "well_info": well,
                "geological_params": well.geological_parameters,
                "production_data": well.production_data,
            }
        return None

    def get_production_for_period(
        self, session: Session, well_name: str, start_date: datetime, end_date: datetime
    ):
        """Получение данных по добыче за период"""
        return (
            session.query(ProductionData)
            .join(Well)
            .filter(
                Well.well_name == well_name,
                ProductionData.date >= start_date,
                ProductionData.date <= end_date,
            )
            .order_by(ProductionData.date)
            .all()
        )

    def get_wells_by_field(self, session: Session, field: str):
        """Получение скважин по месторождению"""
        return session.query(Well).filter(Well.field == field).all()

    def calculate_monthly_production(
        self, session: Session, well_name: str, year: int, month: int
    ):
        """Расчет месячной добычи"""
        from sqlalchemy import extract, func

        result = (
            session.query(
                func.sum(ProductionData.oil_rate).label("total_oil"),
                func.sum(ProductionData.gas_rate).label("total_gas"),
                func.avg(ProductionData.water_cut).label("avg_water_cut"),
            )
            .join(Well)
            .filter(
                Well.well_name == well_name,
                extract("year", ProductionData.date) == year,
                extract("month", ProductionData.date) == month,
            )
            .first()
        )

        return result
