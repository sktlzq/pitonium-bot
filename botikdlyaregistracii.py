import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    FSInputFile,
)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


# ==================
# НАСТРОЙКИ
# ==================

TOKEN = "8598269946:AAGQZcHvIoNltvMV_l2IzOjt-R4E4owYGbY"
ADMIN_ID = 6730606397

# путь к файлу со шпорой
SHPORA_PATH = "shpora.pdf"


bot = Bot(TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)


# ==================
# СОСТОЯНИЯ
# ==================

class Form(StatesGroup):
    name = State()
    grade = State()
    direction = State()
    contact = State()


# ==================
# /START
# ==================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🔥 Записаться на пробное"
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="🎁 Забери шпору и начни подготовку 👇"
    )

    await message.answer(
        text=(
            "🐈 Добро пожаловать в Питониум\n\n"
            "Репетитор по информатике\n"
            "ЕГЭ • ОГЭ • Python • Игры\n\n"
            "Нажми кнопку ниже 👇"
        ),
        reply_markup=kb
    )


# ==================
# СТАРТ АНКЕТЫ
# ==================

@dp.message(F.text == "🔥 Записаться на пробное")
async def begin(message: Message, state: FSMContext):
    await message.answer(
        "Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(Form.name)


# ==================
# ИМЯ
# ==================

@dp.message(Form.name)
async def save_name(message: Message, state: FSMContext):
    await state.update_data(
        name=message.text
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="9 класс"),
                KeyboardButton(text="10 класс")
            ],
            [
                KeyboardButton(text="11 класс")
            ],
            [
                KeyboardButton(text="Другое")
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="🎓 Выбери свой класс"
    )

    await message.answer(
        "Какой ты класс?",
        reply_markup=kb
    )

    await state.set_state(Form.grade)


# ==================
# КЛАСС
# ==================

@dp.message(Form.grade)
async def save_grade(message: Message, state: FSMContext):
    await state.update_data(
        grade=message.text
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ЕГЭ информатика")
            ],
            [
                KeyboardButton(text="ОГЭ информатика")
            ],
            [
                KeyboardButton(text="Python с нуля")
            ],
            [
                KeyboardButton(text="Обучение играм")
            ],
            [
                KeyboardButton(text="Другое")
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="💻 Что интересно изучать?"
    )

    await message.answer(
        "Что тебе интересно?",
        reply_markup=kb
    )

    await state.set_state(Form.direction)


# ==================
# НАПРАВЛЕНИЕ
# ==================

@dp.message(Form.direction)
async def save_direction(message: Message, state: FSMContext):
    await state.update_data(
        direction=message.text
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Отправить номер",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="📱 Нажми кнопку ниже"
    )

    await message.answer(
        "Оставь номер 👇",
        reply_markup=kb
    )

    await state.set_state(Form.contact)


# ==================
# КОНТАКТ
# ==================

@dp.message(Form.contact, F.contact)
async def save_contact(message: Message, state: FSMContext):
    data = await state.get_data()

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "не указан"
    )

    text = f"""
🔥 НОВАЯ ЗАЯВКА

Имя:
{data["name"]}

Класс:
{data["grade"]}

Направление:
{data["direction"]}

Телефон:
{message.contact.phone_number}

Telegram:
{username}

ID:
{message.from_user.id}
"""

    await bot.send_message(
        ADMIN_ID,
        text
    )

    start_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🔥 Записаться на пробное"
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="🐈 Жду тебя снова"
    )

    await message.answer(
        "🐈 Готово!\n\n"
        "Заявка отправлена.\n"
        "Скоро свяжусь 🙌\n\n"
        "А пока держи подарок 🎁",
        reply_markup=start_kb
    )

    try:
        shpora = FSInputFile(SHPORA_PATH)

        await message.answer_document(
            document=shpora,
            caption=(
                "📚 Мини-шпора по ЕГЭ информатике\n\n"
                "Сохрани, чтобы не потерять 🐈"
            )
        )

    except FileNotFoundError:
        await message.answer(
            "⚠️ Файл со шпорой пока не найден.\n"
            "Артём отправит его вручную."
        )

    await state.clear()


# если человек не нажал кнопку с номером, а написал текст
@dp.message(Form.contact)
async def wrong_contact(message: Message):
    await message.answer(
        "Нажми кнопку «📱 Отправить номер» ниже 👇"
    )


# ==================
# ЗАПУСК
# ==================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())