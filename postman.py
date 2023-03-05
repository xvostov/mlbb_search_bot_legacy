import asyncio

import db.functions
from loader import bot
from keyboards.inline import get_like_dislike_kb
from utils import render_msg
from loguru import logger
from aiogram.utils import exceptions


async def send_notification(recipient, profile):
    kb = await get_like_dislike_kb(recipient.user_id, profile.user_id)
    await bot.send_message(recipient.user_id.strip(), render_msg(profile),
                           reply_markup=kb)


def p_filter(profile, pfilter):
    if pfilter:
        if profile.current_rank < pfilter.min_rank:
            return False
        elif profile.current_win_rate < pfilter.min_win_rate:
            return False
        elif profile.voice_communication != pfilter.voice_communication:
            return False

        if pfilter.min_pts:
            # Пропускаем, если в анкете нет птс
            if not profile.current_pts:
                return False
            else:
                if profile.current_pts < pfilter.min_pts:
                    return False
    return True


async def distribution_iteration():
    while True:
        try:
            profiles = await db.functions.get_all_profiles()
            for profile in profiles:
                for recipient in profiles:
                    # Список просмотренных анкет
                    observered_user_ids = [view.observed_user_id for view in recipient.views]

                    # Если анкета и получатель один и тот же человек, пропускаем
                    if recipient.user_id == profile.user_id:
                        continue

                    # Если анкета в списке просмотренных у получателя
                    elif profile.user_id in observered_user_ids:
                        continue

                    recipient_filter = recipient.user_filter
                    profile_filter = profile.user_filter
                    await asyncio.sleep(1)

                    # Фильтруем по предпочтениям получателя анкеты
                    if not p_filter(profile, recipient_filter):
                        continue

                    elif not p_filter(recipient, profile_filter):
                        continue

                    await asyncio.sleep(1)

                    try:
                        logger.debug(f'[{recipient.user_id}] отправляю анкету {profile.user_id}')
                        await send_notification(recipient, profile)

                    except exceptions.BotBlocked:
                        logger.debug(f'[{recipient.user_id}] заблокировал бота')


                    except Exception as err:
                        logger.error(f'[{recipient.user_id}] {err}')
                    else:
                        logger.info(f'[{recipient.user_id}] успешно отправил анкету {profile.user_id}')
                        await db.functions.add_to_viewed(recipient.user_id, profile.user_id)

                    await asyncio.sleep(1)

            await asyncio.sleep(20)

        except Exception as err:
            logger.error(err)
