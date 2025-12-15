from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    create_engine,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()


class Well(Base):
    """Таблица скважин"""

    __tablename__ = "wells"

    id = Column(Integer, primary_key=True)
    well_name = Column(String(50), unique=True, nullable=False)  # Например: "Prod__1"
    field = Column(String(100))  # Месторождение
    area = Column(String(50))  # Участок
    well_type = Column(String(20))  # Добывающая/Нагнетательная
    status = Column(String(20))  # В работе/Консервация/Ликвидирована
    coordinates_x = Column(Float)
    coordinates_y = Column(Float)
    completion_date = Column(DateTime)

    # Связи
    geological_parameters = relationship(
        "GeologicalParameters", back_populates="well", uselist=False
    )
    production_data = relationship("ProductionData", back_populates="well")

    def __repr__(self):
        return f"<Well(id={self.id}, name='{self.well_name}')>"


class GeologicalParameters(Base):
    """Таблица геологических параметров скважин"""

    __tablename__ = "geological_parameters"

    id = Column(Integer, primary_key=True)
    well_id = Column(Integer, ForeignKey("wells.id"), unique=True)

    # Геологические параметры
    porosity = Column(Float)  # Пористость, %
    permeability = Column(Float)  # Проницаемость, мД
    net_pay = Column(Float)  # Эффективная толщина, м
    water_saturation = Column(Float)  # Водонасыщенность, д.ед.
    formation_pressure = Column(Float)  # Пластовое давление, атм
    temperature = Column(Float)  # Температура, °C

    # Связи
    well = relationship("Well", back_populates="geological_parameters")

    # Удобный доступ к имени скважины
    well_name = association_proxy("well", "well_name")

    def __repr__(self):
        return (
            f"<GeologicalParameters(well='{self.well_name}', porosity={self.porosity})>"
        )


class ProductionData(Base):
    """Таблица временных рядов добычи"""

    __tablename__ = "production_data"

    id = Column(Integer, primary_key=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    date = Column(DateTime, nullable=False)  # Дата замера

    # Показатели добычи
    oil_rate = Column(Float)  # Дебит нефти, т/сут
    gas_rate = Column(Float)  # Дебит газа, тыс.м³/сут
    water_rate = Column(Float)  # Дебит воды, м³/сут
    liquid_rate = Column(Float)  # Дебит жидкости, м³/сут
    water_cut = Column(Float)  # Обводненность, %
    gas_oil_ratio = Column(Float)  # Газовый фактор, м³/т

    # Технологические параметры
    bottomhole_pressure = Column(Float)  # Забойное давление, атм
    wellhead_pressure = Column(Float)  # Устьевое давление, атм
    choke_size = Column(Float)  # Штуцер, мм

    # Связи
    well = relationship("Well", back_populates="production_data")

    # Удобный доступ к имени скважины
    well_name = association_proxy("well", "well_name")

    # Композитный индекс для быстрого поиска
    __table_args__ = (Index("idx_well_date", "well_id", "date"),)

    def __repr__(self):
        return f"<ProductionData(well='{self.well_name}', date={self.date}, oil={self.oil_rate})>"
