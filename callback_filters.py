from aiogram.types import CallbackQuery


async def like_dislike_callback_filter(call: CallbackQuery):
    if 'like' or 'dislike' in call.data:
        return True
    else:
        return False