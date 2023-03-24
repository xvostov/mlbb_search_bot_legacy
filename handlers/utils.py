from aiogram.types import CallbackQuery
from utils import get_rank_by_lvl

async def update_data(state, name, value, call=None):
    if call:
        if 'rank' in name:
            await call.answer(f'Вы выбрали: {get_rank_by_lvl(int(call.data))}')

        else:
            await call.answer(f'Вы выбрали: {value}')

        if name == 'role' and value == 'Неважно':
            value = None

    async with state.proxy() as data:
        data[name] = value


def transform_to_boolean(callback: CallbackQuery):
    return True if callback.data == 'да' else False


from aiogram.types import CallbackQuery

async def like_dislike_callback_filter(call: CallbackQuery):
    if 'like' in call.data or 'dislike' in call.data:
        return True
    else:
        return False

