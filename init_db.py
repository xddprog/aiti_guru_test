#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных и тестовых данных
"""
import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from app.infrastructure.database.adapters.pg_connection import DatabaseConnection
from app.utils.init_test_data import init_test_data


async def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация базы данных...")
    
    try:
        # Подключаемся к БД
        db_connection = await DatabaseConnection()()
        session = await db_connection.get_session()
        
        print("📊 Создание тестовых данных...")
        await init_test_data(session)
        
        await session.close()
        print("✅ Инициализация завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
