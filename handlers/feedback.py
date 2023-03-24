from aiogram import types
from .states import FeedBack
from aiogram.dispatcher import FSMContext
from loader import bot
from keyboards.inline import get_contact_kb

async def feedback_cmd_handler(message: types.Message):
    await message.answer('Можете оставить нам обратную связь следующим сообщением')
    await FeedBack.user_fb.set()

async def feedback_handler(message: types.Message, state: FSMContext):
    await message.answer('Спасибо за обратную связь, она будет отправлена')
    await state.finish()

    contact_kb = await get_contact_kb(message.from_user.url)
    await bot.send_message(-995554342, f'ОБРАТНАЯ СВЯЗЬ ОТ ПОЛЬЗОВАТЕЛЯ\nID Пользователя: '
                                       f'{message.from_user.id}\n\n{message.text}', reply_markup=contact_kb)
