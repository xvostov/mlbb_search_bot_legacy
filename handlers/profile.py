from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import ranks_inline_kb, roles_inline_kb, yes_no_kb
from utils import ranks_levels, get_rank_by_lvl
from .states import *
from .utils import update_data, transform_to_boolean
from loader import start_profile_creation, successful_profile_creation, successful_profile_deletion

import db.functions


DEFAULT_VALUE = 'Не указан'

async def new_profile_cmd_handler(message: types.Message):
    profile = await db.functions.get_profile_by_user_id(message.from_user.id)
    if profile:
        await message.answer('У вас уже есть анкета, вы не можете создать новую')
    else:
        await NewProfile.nickname.set()
        await message.answer('[1/10] Отправьте свой никнейм в игре')
        start_profile_creation.inc()


async def new_profile_nickname_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 255:
        await message.answer('Некорректный никней, попробуйте ввести ещё раз')
    else:
        await update_data(state, 'nickname', message.text)
        await state.set_state(NewProfile.last_season_rank)
        await message.answer('[2/10] Выберете ранг прошлого сезона', reply_markup=ranks_inline_kb)


async def last_season_rank_callback_handler(call: CallbackQuery, state: FSMContext):
    last_season_rank = int(call.data)

    await update_data(state, 'last_season_rank', last_season_rank, call)
    await state.set_state(NewProfile.current_rank)
    await call.message.answer('[3/10] Выберете ранг текущего сезона', reply_markup=ranks_inline_kb)


async def current_rank_callback_handler(call: CallbackQuery, state: FSMContext):
    current_rank = int(call.data)

    await update_data(state, 'current_rank', current_rank, call)

    if current_rank > 6:
        await NewProfile.current_pts.set()
        await state.set_state(NewProfile.current_pts)
        await call.message.answer('[4/10] Введите текущее количество pts\nнапример: 1500')
    else:
        await call.message.answer('[5/10] Выберете ваш максимальный ранг', reply_markup=ranks_inline_kb)
        await state.set_state(NewProfile.max_rank)


async def new_profile_current_pts_handler(message: types.Message, state: FSMContext):
    try:
        current_pts = int(message.text)

    except ValueError:
        await message.answer('Вы ввели некорректное число ваших pts очков, попробуйте ещё раз')

    else:
        await update_data(state, 'current_pts', current_pts)

        await state.set_state(NewProfile.max_rank)
        await message.answer('[5/10] Выберете ваш максимальный ранг', reply_markup=ranks_inline_kb)


async def new_profile_max_rank_callback_handler(call: CallbackQuery, state: FSMContext):
    max_rank = int(call.data)

    await update_data(state, 'max_rank', max_rank, call)

    await state.set_state(NewProfile.current_win_rate)
    await call.message.answer('[6/10] Введите текущий вин рейт от 1 до 100\nнапример: 60')


async def new_profile_current_win_rate_handler(message: types.Message, state: FSMContext):
    try:
        current_win_rate = int(message.text)
    except ValueError:
        await message.answer('Вы ввели некорректный вин рейт, попробуйте ещё раз')

    else:
        if 0 < current_win_rate <= 100:
            await update_data(state, 'current_win_rate', current_win_rate)

            await state.set_state(NewProfile.first_role)
            await message.answer('[7/10] Выберете вашу основную роль', reply_markup=roles_inline_kb)

        else:
            await message.answer('Вы ввели некорректный вин рейт, попробуйте ещё раз')


async def new_profile_first_role_callback_handler(call: CallbackQuery, state: FSMContext):
    first_role = call.data
    await update_data(state, 'first_role', first_role, call)

    await state.set_state(NewProfile.second_role)
    await call.message.answer('[8/10] Выберете вашу второстепенную роль', reply_markup=roles_inline_kb)


async def new_profile_second_role_callback_handler(call: CallbackQuery, state: FSMContext):
    second_role = call.data
    await update_data(state, 'second_role', second_role, call)

    await state.set_state(NewProfile.main_characters)
    await call.message.answer('[9/10] Напишите своих основных героев\nнапример: клинт, баданг')


async def new_profile_main_characters(message: types.Message, state: FSMContext):
    await update_data(state, 'main_characters', message.text.strip())
    await state.set_state(NewProfile.voice_communication)
    await message.answer('[10/10] Готовы ли вы общаться по голосовой связи?', reply_markup=yes_no_kb)


async def new_profile_voice_communication_callback_handler(call: CallbackQuery, state: FSMContext):
    await update_data(state, 'voice_communication', call.data, call)

    async with state.proxy() as data:

        # Форматируем вин рейт
        current_win_rate = data.get('current_win_rate', None)
        if current_win_rate:
            current_win_rate = str(current_win_rate) + '%'
        else:
            current_win_rate = 'Не указан'

        profile = f"""
Ваш никнейм: {data.get('nickname', DEFAULT_VALUE)}
Ранг прошлого сезона: {get_rank_by_lvl(data.get('last_season_rank', DEFAULT_VALUE))}
Текущий ранг: {get_rank_by_lvl(data.get('current_rank', DEFAULT_VALUE))}
Текущий pts: {data.get('current_pts', DEFAULT_VALUE)}
Максимальный ранг: {get_rank_by_lvl(data.get('max_rank', DEFAULT_VALUE))}
Текущий вин рейт: {current_win_rate}
Основная роль: {data.get('first_role', DEFAULT_VALUE)}
Второстепенная роль: {data.get('second_role', DEFAULT_VALUE)}
Основные герои: {data.get('main_characters', DEFAULT_VALUE)}
Голосовая связь: {data.get('voice_communication', DEFAULT_VALUE)}

"""
    await call.message.answer(profile.strip())

    await state.set_state(NewProfile.final)
    await call.message.answer('Проверьте вашу анкету, все ли верно указано?', reply_markup=yes_no_kb)


async def new_profile_final_callback_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('OK')
    if not transform_to_boolean(call):

        await call.message.answer('Для повторного заполнения введите команду /new_profile')
        await state.finish()

    else:
        async with state.proxy() as data:
            result = await db.functions.add_profile_to_db(data, call.from_user.id)
        await call.message.answer(result)
        await state.finish()

        if result == 'Ваша анкета успешно сохранена, скоро мы начем вам присылать анкеты других людей.':
            successful_profile_creation.inc()


async def delete_profile_cmd_handler(message: types.Message):
    await DeleteProfile.confirmation.set()
    await message.answer('Вы уверены, что хотите удалить анкету?', reply_markup=yes_no_kb)


async def delete_profile_callback_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('OK')

    if transform_to_boolean(call):
        profile = await db.functions.get_profile_by_user_id(call.from_user.id)
        if profile:
            await db.functions.delete_profile_by_user_id(call.from_user.id)
            await call.message.delete()
            await call.message.answer('Ваша анкета удалена\n\nвы всегда можете создать '
                                      'ее заново с помощью команды: /new_profile')

            successful_profile_deletion.inc()

        else:
            await call.message.answer('У вас ещё нет анкеты, ее можно создать по команду /new_profile')
    else:
        await call.message.answer('Отлично, мы рады, что вы решили остаться с нами')
        await call.message.delete()

    await state.finish()

async def check_profile_handler(message: types):
    profile = await db.functions.get_profile_by_user_id(message.from_user.id)
    if profile:
        msg = f"""
Ваш никнейм: {profile.nickname}\n
Ранг прошлого сезона: {get_rank_by_lvl(profile.last_season_rank)}
Текущий ранг: {get_rank_by_lvl(profile.current_rank)}
Текущий pts: {profile.current_pts if profile.current_pts else DEFAULT_VALUE}
Максимальный ранг: {get_rank_by_lvl(profile.max_rank)}
Текущий вин рейт: {profile.current_win_rate}
Основная роль: {profile.first_role}
Второстепенная роль: {profile.second_role}
Основные герои: {profile.main_characters}
Голосовая связь: {'Да' if profile.voice_communication else 'Нет'}    
""".strip()

        await message.answer(msg)
    else:
        await message.answer('У вас ещё нет анкеты, ее можно создать командой:\n/new_profile')




