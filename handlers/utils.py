from aiogram.types import CallbackQuery
from utils import get_rank_by_lvl


async def update_data(state, name, value, call=None):
    if call:
        if 'rank' in name:
            await call.answer(f'Вы выбрали: {get_rank_by_lvl(int(call.data))}')
        else:
            await call.answer(f'Вы выбрали: {value}')
    async with state.proxy() as data:
        data[name] = value


def transform_to_boolean(callback: CallbackQuery):
    return True if callback.data == 'да' else False
