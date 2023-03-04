from aiogram.dispatcher.filters.state import State, StatesGroup

class NewProfile(StatesGroup):
    nickname = State()
    last_season_rank = State()
    current_rank = State()
    current_pts = State()
    max_rank = State()
    current_win_rate = State()
    first_role = State()
    second_role = State()
    main_characters = State()
    voice_communication = State()
    final = State()


class DeleteProfile(StatesGroup):
    confirmation = State()


class NewFilter(StatesGroup):
    min_rank = State()
    min_pts = State()
    min_win_rate = State()
    voice_communication = State()
    final = State()

class DeleteFilter(StatesGroup):
    confirmation = State()


class FeedBack(StatesGroup):
    user_fb = State()

class AdminNotification(StatesGroup):
    notification = State()