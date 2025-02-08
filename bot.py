import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен бота
TOKEN = "ТОКЕН_ИЗ_BOTFATHER"

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🔐 Привет! Я SecureBot.\n"
        "Я помогу тебе проверить безопасность сайтов и серверов.\n"
        "🔍 Отправь мне URL, и я начну анализ."
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
