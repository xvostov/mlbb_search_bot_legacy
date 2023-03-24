from aiogram import types

from aiogram.dispatcher import FSMContext
from loader import bot
from loguru import logger
from .states import AdminNotification

import db.functions


async def say_all_cmd_handler(message: types.Message):
    user = await db.functions.get_user_by_id(message.from_user.id)

    if user.is_admin is True:
        await message.answer('Напишите текст оповещения')
        await AdminNotification.notification.set()
    else:
        await message.answer('У вас нет доступа к этой команде')


async def notification_handler(message: types.Message, state: FSMContext):
    users = await db.functions.get_all_users()

    err_counter = 0
    for user in users:

        try:
            chat = await bot.get_chat(user.user_id)
            await chat.unpin_all_messages()

        except Exception:
            pass

        try:
            logger.debug(f'Пытаюсь отправить оповещение {user.user_id}')
            msg = await bot.send_message(user.user_id, message.text)
        except Exception:
            await message.answer(f'Не удалось оповестить {user.user_id}')
            logger.warning(f'Не удалось оповестить {user.user_id}')
            err_counter += 1
        else:
            logger.debug(f'Успешно оповестил {user.user_id}')
            await bot.pin_chat_message(user.user_id, msg.message_id)

    if err_counter == 0:
        await message.answer('Всех успешно оповестили')
        logger.info('Всех успешно оповестили')
    else:
        await message.answer('Не всех удалось оповестить')
        logger.warning(f'Не всех удалось оповестить, не удалось отправить: {err_counter} людям')

    await state.finish()
