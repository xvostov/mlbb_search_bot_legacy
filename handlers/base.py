from aiogram import types
from aiogram.types import CallbackQuery
import db.functions
import db.utils
from loader import start_cmd_counter
from loguru import logger


with open('rules.txt', 'r', encoding='utf-8') as f_o:
    rules_txt = f_o.read()


async def start_cmd_handler(message: types.Message):
    await message.answer("Привет, здесь ты сможешь найти партнера\n"
                         "для игры в Mobile Legends Bang Bang.\n\n"
                         "Перед началом использования ознакомьтесь с правилами, команда /rules,\n\n"
                         "Создать анкету можно командой /new_profile\n\n"
                         "Полный список доступных команд с описанием можно посмотреть в выпадающем меню,"
                         " слева от поля для ввода сообщения")

    logger.debug(f'Пользователь {message.from_user.id} нажал start')

    user = await db.functions.get_user_by_id(message.from_user.id)
    if not user:
        user = db.utils.create_user(message)

        logger.debug(f'Adding user in db: {user}')

        await db.functions.add_user(user)

        start_cmd_counter.inc()


async def rules_cmd_handler(message: types.Message):
    await message.answer(rules_txt)


# Заглушка, срабатывает, если callback без контекста
async def callback_handler_without_context(call: CallbackQuery):
    await call.answer('Сейчас это нельзя выбрать 😅')
