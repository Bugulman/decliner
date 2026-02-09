# Automaticaly recalculate=true
# Single model=false
import logging
import os
import shutil
import time
from pathlib import Path

import schedule

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_copy.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def copy_files(from_filepath, to_filepath):
    """
    Копирование файлов из одной директории в другую

    :param from_filepath: Путь к исходной директории
    :param to_filepath: Путь к целевой директории
    """
    try:
        # Проверка существования исходной директории
        if not os.path.exists(from_filepath):
            logger.error(f"Исходная директория не существует: {from_filepath}")
            return False

        # Создание целевой директории, если она не существует
        Path(to_filepath).mkdir(parents=True, exist_ok=True)

        # Счетчики
        copied_files = 0
        error_files = 0

        # Используем pathlib для безопасной работы с путями
        source_path = Path(from_filepath)
        target_path = Path(to_filepath)

        logger.info(f"Начинаю копирование из {source_path} в {target_path}")

        # Рекурсивное копирование файлов
        for file_path in source_path.rglob("*"):
            if file_path.is_file():
                try:
                    # Создаем соответствующую структуру папок в целевой директории
                    relative_path = file_path.relative_to(source_path)
                    target_file_path = target_path / relative_path

                    # Создаем директории, если они не существуют
                    target_file_path.parent.mkdir(parents=True, exist_ok=True)

                    # Копируем файл
                    shutil.copy2(file_path, target_file_path)
                    logger.debug(f"Скопирован файл: {file_path}")
                    copied_files += 1

                except Exception as e:
                    logger.error(f"Ошибка копирования файла {file_path}: {str(e)}")
                    error_files += 1

        logger.info(
            f"Копирование завершено. Успешно: {copied_files}, Ошибок: {error_files}"
        )
        return True

    except Exception as e:
        logger.error(f"Ошибка в функции copy_files: {str(e)}")
        return False


def safe_copy_files(from_filepath, to_filepath):
    """
    Обертка для копирования с дополнительной проверкой
    """
    try:
        return copy_files(from_filepath, to_filepath)
    except Exception as e:
        logger.error(f"Критическая ошибка при копировании: {str(e)}")
        return False


# Настройка расписания
schedule.every().day.at("05:00").do(
    safe_copy_files,
    from_filepath="m:/dell-3x36-gpu/cc02/MINN_15.12_SCH/RESULTS/",
    to_filepath="D:/project/Minnib_project/SCHED_PATTERNS/RESULTS/",
)

logger.info("Скрипт запущен. Ожидание выполнения по расписанию...")

# Основной цикл
try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("Скрипт остановлен пользователем")
except Exception as e:
    logger.error(f"Неожиданная ошибка: {str(e)}")
