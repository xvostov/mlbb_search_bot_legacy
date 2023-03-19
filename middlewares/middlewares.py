from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import db.functions

class UserBlockMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await db.functions.get_user_by_id(message.from_user.id)

        if user.is_active is False:
            await message.answer('Ваш аккаунт деактивирован.')
            raise CancelHandler()

        return True