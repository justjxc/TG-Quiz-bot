import asyncio
import logging
from bot_init import dp, bot
from functions.db_functions import create_table

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main():
    # Запускаем создание таблицы базы данных
    await create_table()

    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())