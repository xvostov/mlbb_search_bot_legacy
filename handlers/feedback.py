from aiogram import types
from .states import FeedBack
from aiogram.dispatcher import FSMContext
from loader import bot

async def feedback_cmd_handler(message: types.Message):
    await message.answer('Можете оставить нам обратную связь следующим сообщением')
    await FeedBack.user_fb.set()

async def feedback_handler(message: types.Message, state: FSMContext):
    await message.answer('Спасибо за обратную связь, она будет отправлена')
    await state.finish()

    await bot.send_message(767684418, f'ОБРАТНАЯ СВЯЗЬ ОТ ПОЛЬЗОВАТЕЛЯ\nID Пользователя: {message.from_user.id}\n\n{message.text}')
