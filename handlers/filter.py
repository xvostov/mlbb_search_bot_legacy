from aiogram.dispatcher import FSMContext
from aiogram import types
from .states import NewFilter, DeleteFilter
from .utils import update_data, transform_to_boolean
import db.functions
from utils import get_rank_by_lvl

from keyboards.inline import ranks_inline_kb, yes_no_kb

DEFAULT_VALUE = 'Не указан'

async def new_filter_cmd_handler(message: types.Message):
    profile = await db.functions.get_profile_by_user_id(message.from_user.id)

    if profile:
        user_filter = profile.user_filter

    if not profile:
        await message.answer('У вас ещё нет анкеты, создайте ее через команду /new_profile')

    elif user_filter:

        await message.answer('У вас уже есть активный фильтр! Для создания нового фильтра удалите старый. Команда для удаления: /delete_filter')

    else:
        await NewFilter.min_rank.set()
        await message.answer('[1/4] Выберете минимальный ранг игрока, который вас интересует', reply_markup=ranks_inline_kb)

async def new_filter_min_rank(call: types.CallbackQuery, state: FSMContext):
    min_rank = int(call.data)
    await update_data(state, 'min_rank', min_rank, call)

    if min_rank > 6:
        await state.set_state(NewFilter.min_pts)
        await call.message.answer('[2/4] Введите минимальный pts, который вас интересует\nнапример: 1500')

    else:
        await state.set_state(NewFilter.min_win_rate)
        await call.message.answer('[3/4] Введите минимальный вин рейт, который вас интересует\nнапример: 55')

async def new_filter_min_pts_handler(message: types.Message, state: FSMContext):
    try:
        current_pts = int(message.text)

    except ValueError:
        await message.answer('Вы ввели некорректное число ваших pts очков, попробуйте ещё раз')

    else:
        await update_data(state, 'min_pts', current_pts)
        await state.set_state(NewFilter.min_win_rate)
        await message.answer('[3/4] Введите минимальный вин рейт, который вас интересует\nнапример: 55')

async def new_filter_min_win_rate_handler(message: types.Message, state: FSMContext):
    try:
        min_win_rate = int(message.text)
    except ValueError:
        await message.answer('Вы ввели некорректный вин рейт, попробуйте ещё раз')

    else:
        if 0 < min_win_rate <= 100:
            await update_data(state, 'min_win_rate', min_win_rate)
            await state.set_state(NewFilter.voice_communication)
            await message.answer('[4/4] Нужен человек с голосовым чатом?', reply_markup=yes_no_kb)

        else:
            await message.answer('Вы ввели некорректный вин рейт, попробуйте ещё раз')

async def new_filter_voice_communication_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await update_data(state, 'voice_communication', call.data, call)

    async with state.proxy() as data:
        # Форматируем вин рейт
        min_win_rate = data.get('min_win_rate', None)
        if min_win_rate:
            min_win_rate = str(min_win_rate) + '%'
        else:
            min_win_rate = 'Не указан'

        filter_msg = f"""
Ваши предпочтения:

Минимальный ранг: {get_rank_by_lvl(data.get('min_rank', DEFAULT_VALUE))}
Минимальный pts: {data.get('min_pts', DEFAULT_VALUE)}
Минимальный вин рейт: {min_win_rate}
Голосовая связь: {data.get('voice_communication', DEFAULT_VALUE)}

"""
    await call.message.answer(filter_msg.strip())

    await state.set_state(NewFilter.final)
    await call.message.answer('Проверьте установленные настройки фильтра, все ли верно указано?', reply_markup=yes_no_kb)

async def new_filter_final_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('OK')
    if not transform_to_boolean(call):

        await call.message.answer('Для повторного заполнения введите команду /new_filter')
        await state.finish()

    else:
        async with state.proxy() as data:
            result = await db.functions.add_user_filter_to_db(data, call.from_user.id)
        await call.message.answer(result)
        await state.finish()

async def delete_filter_cmd_handler(message: types.Message):
    await DeleteFilter.confirmation.set()
    await message.answer('Вы уверены, что хотите удалить фильтр?', reply_markup=yes_no_kb)


async def delete_filter_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('OK')

    if transform_to_boolean(call):
        await db.functions.delete_filter_by_user_id(call.from_user.id)
        await call.message.delete()
        await call.message.answer('Ваш фильтр удален')

    else:
        await call.message.answer('Хорошо, вы всегда можете удалить настройки фильтра и '
                                  'создать новые командой /new_filter')
        await call.message.delete()

    await state.finish()

async def check_filter(message: types.Message):
    user_filter = await db.functions.get_user_filter_by_user_id(message.from_user.id)
    if user_filter:
        msg = f"""
Ваши предпочтения:

Минимальный ранг: {get_rank_by_lvl(user_filter.min_rank)}
Минимальный pts: {user_filter.min_pts if user_filter.min_pts else DEFAULT_VALUE}
Минимальный вин рейт: {user_filter.min_win_rate}
Голосовая связь: {'Да' if user_filter.voice_communication else 'Нет'}
""".strip()

        await message.answer(msg)

    else:
        await message.answer('У вас ещё нет фильтра\nвы можете создать используя команду /new_filter')