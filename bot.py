import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from crud import add_site, get_average_prices
from parser import run_parsing

load_dotenv()
TOKEN = os.getenv("TOKEN")
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR", "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Загрузить файл")],
        [KeyboardButton(text="Спарсить")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Пришли мне Excel-файл с сайтами.", reply_markup=keyboard
    )

@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    document = message.document
    file_path = os.path.join(DOWNLOADS_DIR, document.file_name)
    await bot.download(document, destination=file_path)
    df = pd.read_excel(file_path)
    await message.answer(f"Файл загружен!\n\n{df.head().to_string()}")
    for _, row in df.iterrows():
        add_site(row["title"], row["url"], row["xpath"])
    await message.answer("Сайты добавлены в базу данных!")

@dp.message(lambda message: message.text == "Средняя цена")
async def send_average_prices(message: types.Message):
    results = get_average_prices()
    text = "\n".join(
        [f"{title}: {avg_price:.2f} руб." for title, avg_price in results]
    )
    await message.answer(text or "Цены пока не загружены.")

@dp.message(lambda message: message.text == "Спарсить")
async def parse_and_send(message: types.Message):
    await message.answer("🔄 Запускаю парсинг...")
    run_parsing()
    results = get_average_prices()
    if not results:
        await message.answer("⚠️ Данные о ценах пока отсутствуют.")
        return
    text = "Средние цены:\n" + "\n".join(
        [f"{title}: {avg_price:.2f} ₽" for title, avg_price in results]
    )
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
