from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


class DatabaseManager:
    def __init__(self, connection_string="sqlite:///wells_database.db"):
        """Инициализация подключения к БД"""
        self.engine = create_engine(connection_string, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self):
        """Создание всех таблиц"""
        Base.metadata.create_all(bind=self.engine)
        print("Таблицы успешно созданы")

    def get_session(self):
        """Получение сессии"""
        return self.SessionLocal()


# Для PostgreSQL используйте:
# postgresql://user:password@localhost/wells_db
# Для SQLite (по умолчанию):
# sqlite:///wells_database.db
# connection_string="duckdb:///my_database.duckdb"
