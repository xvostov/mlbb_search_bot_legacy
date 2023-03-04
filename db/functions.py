from aiogram.dispatcher.storage import FSMContextProxy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from .models import *


from loader import DB_ENGINE


async def add_profile_to_db(profile_data: FSMContextProxy, user_id):
    try:
        with sessionmaker(bind=DB_ENGINE)() as session:
            session.add(Profile(
                user_id=user_id,
                nickname=profile_data.get('nickname'),
                last_season_rank=profile_data.get('last_season_rank'),
                current_rank=profile_data.get('current_rank'),
                current_pts=profile_data.get('current_pts', None),
                max_rank=profile_data.get('max_rank'),
                current_win_rate=profile_data.get('current_win_rate'),
                first_role=profile_data.get('first_role'),
                second_role=profile_data.get('second_role'),
                main_characters=profile_data.get('main_characters'),
                voice_communication=True if profile_data.get('voice_communication') == 'да' else False
            ))
            session.commit()

    except Exception as err:
        return 'Не удалось сохранить вашу анкету, попробуйте позже'

    else:
        return 'Ваша анкета успешно сохранена, скоро мы начем вам присылать анкеты других людей.'


async def get_profile_by_user_id(user_id):
    with sessionmaker(bind=DB_ENGINE)() as session:
        try:
            profile = session.query(Profile).filter(Profile.user_id == int(user_id)).one()
        except NoResultFound:
            return None
        else:
            return profile


async def delete_profile_by_user_id(user_id):
    with sessionmaker(bind=DB_ENGINE)() as session:
        session.query(Profile).filter(Profile.user_id == int(user_id)).delete()
        session.commit()


async def get_all_profiles():
    with sessionmaker(bind=DB_ENGINE)() as session:
        return session.query(Profile).all()

async def get_profiles_by_filter(user_filter: UserFilter):
    with sessionmaker(bind=DB_ENGINE)() as session:
        if user_filter.min_pts:
            return session.query(Profile).filter(Profile.current_rank >= user_filter.min_rank,
                                                 Profile.current_pts >= user_filter.min_pts,
                                                 Profile.current_win_rate >= user_filter.min_win_rate,
                                                 Profile.voice_communication == user_filter.voice_communication).all()

        else:
            return session.query(Profile).filter(Profile.current_rank >= user_filter.min_rank,
                                                 Profile.current_win_rate >= user_filter.min_win_rate,
                                                 Profile.voice_communication == user_filter.voice_communication).all()

async def add_to_viewed(observer_user_id, observered_user_id):
    with sessionmaker(bind=DB_ENGINE)() as session:
        session.add(View(
            observer_user_id=observer_user_id,
            observed_user_id=observered_user_id
        ))
        session.commit()


async def add_user_filter_to_db(filter_data, user_id):
    try:
        with sessionmaker(bind=DB_ENGINE)() as session:
            session.add(UserFilter(
                user_id=user_id,
                min_rank=filter_data.get('min_rank'),
                min_pts=filter_data.get('min_pts', None),
                min_win_rate=filter_data.get('min_win_rate'),
                voice_communication=True if filter_data.get('voice_communication') == 'да' else False
            ))
            session.commit()

    except Exception as err:
        return 'Не удалось сохранить ваш фильтр, попробуйте позже'

    else:
        return 'Ваш фильтр сохранен'

async def delete_filter_by_user_id(user_id):
    with sessionmaker(bind=DB_ENGINE)() as session:
        session.query(UserFilter).filter(UserFilter.user_id == int(user_id)).delete()
        session.commit()


async def get_user_filter_by_user_id(user_id):
    with sessionmaker(bind=DB_ENGINE)() as session:
        try:
            user_filter = session.query(UserFilter).filter(UserFilter.user_id == int(user_id)).one()
        except NoResultFound:
            return None
        else:
            return user_filter