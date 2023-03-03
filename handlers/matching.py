import db.functions

from aiogram.types import CallbackQuery
from keyboards.inline import get_contact_kb
from loader import bot
from utils import render_msg


async def like_dislike_callback_handler(call: CallbackQuery):
    await call.answer(call.data.split(':')[1])

    user_id, reaction, recipient = call.data.split(':')

    if reaction == 'dislike':
        await call.message.delete()

    else:
        await call.message.delete_reply_markup()
        await bot.send_message(recipient, 'Ура! Твоя анкета кому-то понравилась, вот анкета этого человека ')

        profile = await db.functions.get_profile_by_user_id(user_id)

        contact_kb = await get_contact_kb(call.from_user.url)
        await bot.send_message(recipient, render_msg(profile), reply_markup=contact_kb)