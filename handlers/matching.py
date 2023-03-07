import db.functions
from loguru import logger
from aiogram.types import CallbackQuery
from keyboards.inline import get_contact_kb
from loader import bot
from utils import render_msg


async def like_dislike_callback_handler(call: CallbackQuery):
    data = call.data.split(':')
    try:
        await call.answer(data[1])
    except IndexError:
        logger.error(f'IndexError: call_data: {data}')

    else:

        user_id, reaction, recipient = call.data.split(':')

        if reaction == 'dislike':
            await call.message.delete()

        else:
            await call.message.delete_reply_markup()
            await bot.send_message(recipient, 'Ура! Твоя анкета кому-то понравилась, вот анкета этого человека ')
            logger.debug(f'Успешно отправил контакты {user_id} пользователю с id: {recipient}')

            profile = await db.functions.get_profile_by_user_id(user_id)

            logger.debug(f'Создаю кнопку написать. id анкеты: {call.from_user.id} Получатель: {recipient}')
            contact_kb = await get_contact_kb(call.from_user.url)
            await bot.send_message(recipient, render_msg(profile), reply_markup=contact_kb)