def render_msg(profile):
    msg = f"""
{profile.nickname}

Ранг прошлого сезона: {get_rank_by_lvl(profile.last_season_rank)}
Текущий ранг: {get_rank_by_lvl(profile.last_season_rank)}
Текущий pts: {profile.current_pts if isinstance(profile.current_pts, int) else 'Не указан'}
Максимальный ранг: {get_rank_by_lvl(profile.max_rank)}
Текущий вин рейт: {profile.current_win_rate}
Основная роль: {profile.first_role}
Второстепенная роль: {profile.second_role}
Основные герои: {profile.main_characters}
Голосовая связь: {'Да' if profile.voice_communication else 'Нет'}
"""
    return msg


ranks_levels = {'Воин': 1,
                'Элита': 2,
                'Мастер': 3,
                'Грандмастер': 4,
                'Эпический': 5,
                'Легенда': 6,
                'Мифический': 7,
                'Мифическая слава': 8}

def get_rank_by_lvl(lvl):
    for key in list(ranks_levels.keys()):
        if lvl == ranks_levels.get(key):
            return key
