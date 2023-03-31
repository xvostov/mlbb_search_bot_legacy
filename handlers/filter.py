from aiogram.dispatcher import FSMContext
from aiogram import types
from .states import NewFilter, DeleteFilter
from .utils import update_data, transform_to_boolean
import db.functions
from utils import get_rank_by_lvl
from db.models import UserFilter
from typing import Union

from keyboards.inline import ranks_inline_kb, yes_no_kb, roles_inline_kb_for_filter

DEFAULT_VALUE = 'Не указан'


async def new_filter_cmd_handler(message: Union[types.Message, types.CallbackQuery]):
    profile = await db.functions.get_profile_by_user_id(message.from_user.id)

    print(profile)
    if not profile:
        await message.answer('У вас ещё нет анкеты, создайте ее через команду /new_profile')
    else:
        user_filter = await db.functions.get_filter_by_user_id(profile.user_id)
        if user_filter:

            await message.answer('У вас уже есть активный фильтр! Для создания нового фильтра удалите старый. '
                                 'Команда для удаления: /delete_filter')

        else:
            await NewFilter.min_rank.set()
            await message.answer('[1/4] Выберете минимальный ранг игрока, который вас интересует',
                                 reply_markup=ranks_inline_kb)


async def new_filter_min_rank(call: types.CallbackQuery, state: FSMContext):
    min_rank = int(call.data)
    await update_data(state, 'min_rank', min_rank, call)

    if min_rank > 6:
        await state.set_state(NewFilter.min_pts)
        await call.message.answer('[2/4] Введите минимальный pts, который вас интересует\nнапример: 1500')

    else:
        await state.set_state(NewFilter.min_win_rate)
        await call.message.answer('[3/4] Введите минимальный винрейт, который вас интересует\nнапример: 55')


async def new_filter_min_pts_handler(message: types.Message, state: FSMContext):
    try:
        current_pts = int(message.text)

    except ValueError:
        await message.answer('Вы ввели некорректное число ваших pts очков, попробуйте ещё раз')

    else:
        await update_data(state, 'min_pts', current_pts)
        await state.set_state(NewFilter.min_win_rate)
        await message.answer('[3/4] Введите минимальный винрейт, который вас интересует\nнапример: 55')


async def new_filter_min_win_rate_handler(message: types.Message, state: FSMContext):
    try:
        min_win_rate = int(message.text)
    except ValueError:
        await message.answer('Вы ввели некорректный винрейт, попробуйте ещё раз')

    else:
        if 0 < min_win_rate <= 100:
            await update_data(state, 'min_win_rate', min_win_rate)
            await state.set_state(NewFilter.role)
            await message.answer('[4/4] Выберете роль, которую вы ищите', reply_markup=roles_inline_kb_for_filter)

        else:
            await message.answer('Вы ввели некорректный винрейт, попробуйте ещё раз')


async def new_filter_role_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await update_data(state, 'role', call.data, call)

    async with state.proxy() as data:
        # Форматируем винрейт
        min_win_rate = data.get('min_win_rate', None)
        if min_win_rate:
            min_win_rate = str(min_win_rate) + '%'
        else:
            min_win_rate = 'Не указан'

        filter_msg = f"""
Ваши предпочтения:

Минимальный ранг: {get_rank_by_lvl(data.get('min_rank', DEFAULT_VALUE))}
Минимальный pts: {data.get('min_pts', DEFAULT_VALUE)}
Минимальный винрейт: {min_win_rate}
Ищем роль: {data.get('role', DEFAULT_VALUE)}

"""
    await call.message.answer(filter_msg.strip())

    await state.set_state(NewFilter.final)
    await call.message.answer('Проверьте установленные настройки фильтра, все ли верно указано?',
                              reply_markup=yes_no_kb)


async def new_filter_final_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('OK')
    if not transform_to_boolean(call):

        await call.message.answer('Для повторного заполнения введите команду /new_filter')
        await state.finish()

    else:
        async with state.proxy() as data:
            user_filter = UserFilter(
                user_id=call.from_user.id,
                min_rank=data.get('min_rank'),
                min_pts=data.get('min_pts', None),
                min_win_rate=data.get('min_win_rate'),
                role=data.get('role', None)
            )

            try:
                await db.functions.add_filter_to_db(user_filter)
            except Exception:
                await call.message.answer('Не удалось сохранить свой фильтр, попробуйте попозже')

            else:
                await call.message.answer('Ваш фильтр успешно сохранен')
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
    user_filter: UserFilter = await db.functions.get_filter_by_user_id(message.from_user.id)

    if user_filter:
        msg = f"""
Ваши предпочтения:

Минимальный ранг: {get_rank_by_lvl(user_filter.min_rank)}
Минимальный pts: {user_filter.min_pts if user_filter.min_pts else DEFAULT_VALUE}
Минимальный винрейт: {user_filter.min_win_rate}
Ищем роль: {user_filter.role}
""".strip()

        await message.answer(msg)

    else:
        await message.answer('У вас ещё нет фильтра\nвы можете создать используя команду /new_filter')
