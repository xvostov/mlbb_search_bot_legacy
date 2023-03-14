from aiogram import types
from aiogram.types import CallbackQuery
import db.functions
from loader import start_cmd_counter

with open('rules.txt', 'r', encoding='utf-8') as f_o:
    rules_txt = f_o.read()


async def start_cmd_handler(message: types.Message):
    await message.answer("Привет, здесь ты сможешь найти партнера\n"
                         "для игры в Mobile Legends Bang Bang.\n\n"
                         "Перед началом использования ознакомьтесь с правилами, команда /rules,\n\n"
                         "Создать анкету можно командой /new_profile\n\n"
                         "Полный список доступных команд с описанием можно посмотреть в выпадающем меню,"
                         " слева от поля для ввода сообщения")

    profile = await db.functions.get_profile_by_user_id(message.from_user.id)
    if not profile:
        start_cmd_counter.inc()


async def rules_cmd_handler(message: types.Message):
    await message.answer(rules_txt)


async def donate_cmd_handler(message: types.Message):
    await message.answer("""
Если вам понравился наш проект, у вас есть возможность его поддержать и помочь нам сделать его еще лучше! 
Ваше пожертвование поможет нам развиваться, добавлять новые функции и улучшать пользовательский опыт. 
Пожертвование можно сделать легко и безопасно 
с помощью сервиса от Яндекса по ссылке ниже.

https://donate.stream/mlbb_search_bot

    """)

# Заглушка, срабатывает, если callback без контекста
async def callback_handler_without_context(call: CallbackQuery):
    await call.answer('Сейчас это нельзя выбрать 😅')