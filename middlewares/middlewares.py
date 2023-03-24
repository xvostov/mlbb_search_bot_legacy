from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import db.functions
import db.utils

from loguru import logger

class UserBlockMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.from_user.is_bot is True:
            raise CancelHandler


        print(f'x: {message.from_user.id}')
        user = await db.functions.get_user_by_id(message.from_user.id)

        try:
            if user.is_active is False:
                await message.answer('Ваш аккаунт деактивирован.\n\nМожете оставить ваше обращения по email:\n\nmlbb.search.bot.official@gmail.com')
                raise CancelHandler()
        except AttributeError:
            user = await db.functions.get_user_by_id(message.from_user.id)
            if not user:
                user = db.utils.create_user(message)

                logger.debug(f'Adding user in db: {user}')

                await db.functions.add_user(user)

        return True