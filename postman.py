import asyncio
import db.functions
from db.models import Profile, UserFilter, View
from loader import bot
from keyboards.inline import get_like_dislike_kb
from loguru import logger
from aiogram.utils import exceptions
from utils import render_msg


async def send_notification(recipient, profile):
    kb = await get_like_dislike_kb(recipient.user_id, profile.user_id)
    await bot.send_message(recipient.user_id, render_msg(profile),
                           reply_markup=kb)


def p_filter(profile: Profile, pfilter: UserFilter, owner_filter: Profile, check_role=False):
    if pfilter:

        if profile.current_rank < pfilter.min_rank:
            logger.debug(
                f'[{owner_filter.user_id}] У {profile.user_id} ранг меньше {pfilter.min_rank}({profile.current_rank}), фильтрую')
            return False
        elif profile.current_win_rate < pfilter.min_win_rate:
            logger.debug(
                f'[{owner_filter.user_id}] У {profile.user_id} вр меньше {pfilter.min_win_rate}({profile.current_win_rate}), фильтрую')
            return False

        if pfilter.min_pts:
            # Пропускаем, если в анкете нет птс
            if not profile.current_pts:
                logger.debug(f'[{owner_filter.user_id}] У {profile.user_id} нет птс, а фильтре есть, фильтрую')
                return False
            else:
                if profile.current_pts < pfilter.min_pts:
                    logger.debug(
                        f'[{owner_filter.user_id}] У {profile.user_id} птс меньше {pfilter.min_pts}({profile.current_pts}), фильтрую')
                    return False

        if check_role is True:
            if pfilter.role:
                profile_roles = [profile.first_role, profile.second_role]
                if pfilter.role not in profile_roles:
                    logger.debug(f'Фильтрую, так как искомая роль: {pfilter.role}, а у профиля: {", ".join(profile_roles)}')
                    return False

    return True


async def distribution_iteration():
    while True:
        logger.info('Начал новую итерацию распространения')
        try:
            profiles = await db.functions.get_all_profiles()
            for profile in profiles:
                logger.debug(f'Делаю рассылку профиля: {profile.user_id}')
                profile_filter = await db.functions.get_filter_by_user_id(profile.user_id)
                for recipient in profiles:
                    logger.debug(f'Проверяю может ли {recipient.user_id} быть получателем анкеты {profile.user_id}')

                    # Фильтруем получателя, если его регион не подходит
                    if recipient.region != profile.region:
                        logger.debug(
                            f'Фильтрую, так как регион получателя: {recipient.region}, а у профиля: {profile.region}')
                        continue

                    # Список просмотренных анкет
                    recipient_views = await db.functions.get_view_of_profile(recipient.user_id)
                    observered_user_ids = [view.observed_user_id for view in recipient_views]

                    # Если анкета и получатель один и тот же человек, пропускаем
                    if recipient.user_id == profile.user_id:
                        continue

                    # Если анкета в списке просмотренных у получателя
                    elif profile.user_id in observered_user_ids:
                        logger.debug(f'Анкета {profile.user_id} в списке просмотренный пользователя {recipient.user_id}')
                        continue

                    recipient_filter = await db.functions.get_filter_by_user_id(recipient.user_id)

                    # Фильтруем по предпочтениям получателя анкеты
                    if not p_filter(profile, recipient_filter, recipient, check_role=True):
                        logger.debug(f'Анкета {profile.user_id} не подошла по фильтру {recipient.user_id}')
                        continue

                    elif not p_filter(recipient, profile_filter, profile):
                        logger.debug(f'Получатель {recipient.user_id} не подошел по фильтру анкеты {profile.user_id}')
                        continue

                    try:
                        logger.debug(f'Отправляю анкету {profile.user_id}] получателю {recipient.user_id}')
                        await send_notification(recipient, profile)

                    except exceptions.BotBlocked:
                        logger.debug(f'Получатель {recipient.user_id} заблокировал бота')


                    except Exception as err:
                        logger.error(f'[{recipient.user_id}] {err}')
                    else:
                        logger.info(f'Успешно отправил анкету {profile.user_id} получателю {recipient.user_id}')
                        view = View(
                            observer_user_id=recipient.user_id,
                            observed_user_id=profile.user_id,
                        )
                        await db.functions.add_to_viewed(view)

            logger.info('Закончил итерацию распространения')
            await asyncio.sleep(20)

        except Exception as err:
            logger.error(err)
