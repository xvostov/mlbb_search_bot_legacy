from aiogram import types
from .states import FeedBack
from aiogram.dispatcher import FSMContext
from loader import bot
from loguru import logger
from .states import AdminNotification

import db.functions

async def say_all_cmd_handler(message: types.Message):
    if str(message.from_user.id) == '767684418':
        await message.answer('Напишите текст оповещения')
        await AdminNotification.notification.set()
    else:
        await message.answer('У вас нет доступа к этой команде')


async def notification_handler(message: types.Message, state: FSMContext):
    profiles = await db.functions.get_all_profiles()

    err_counter = 0
    for profile in profiles:
        try:
            logger.debug(f'Пытаюсь отправить оповещение {profile.user_id}')
            msg = await bot.send_message(profile.user_id, message.text)
        except Exception:
            await message.answer(f'Не удалось оповестить {profile.user_id}')
            logger.warning(f'Не удалось оповестить {profile.user_id}')
            err_counter += 1
        else:
            logger.debug(f'Успешно оповестил {profile.user_id}')
            await bot.pin_chat_message(profile.user_id, msg.message_id)

    if err_counter == 0:
        await message.answer('Всех успешно оповестили')
        logger.info('Всех успешно оповестили')
    else:
        await message.answer('Не всех удалось оповестить')
        logger.warning(f'Не всех удалось оповестить, не удалось отправить: {err_counter} людям')

    await state.finish()