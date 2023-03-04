import asyncio

import db.functions
from loader import bot
from keyboards.inline import get_like_dislike_kb
from utils import render_msg
from loguru import logger
from aiogram.utils import exceptions
from loader import bot_blockers
async def send_notification(recipient, profile):
    kb = await get_like_dislike_kb(recipient.user_id, profile.user_id)
    await bot.send_message(recipient.user_id, render_msg(profile),
                           reply_markup=kb)

async def distribution_iteration():
    while True:
        print(bot_blockers)
        profiles = await db.functions.get_all_profiles()

        for profile in profiles:
            if profile.user_id in bot_blockers:
                continue

            for recipient in profiles:
                if recipient.user_id in bot_blockers:
                    continue

                observered_user_ids = [view.observed_user_id for view in recipient.views]

                if recipient.user_id == profile.user_id:
                    continue

                elif profile.user_id in observered_user_ids:
                    continue

                if recipient.user_filter:
                    user_filter = recipient.user_filter

                    if profile.current_rank < user_filter.min_rank:
                        continue
                    elif profile.current_win_rate < user_filter.min_win_rate:
                        continue
                    elif profile.voice_communication != user_filter.voice_communication:
                        continue

                    if user_filter.min_pts:
                        if not profile.current_pts:
                            continue
                        else:
                            if profile.current_pts < user_filter.min_pts:
                                continue

                    try:
                        logger.debug(f'[{recipient.user_id}] отправляю анкету {profile.user_id}')
                        await send_notification(recipient, profile)

                    except exceptions.BotBlocked:
                        logger.debug(f'[{recipient.user_id}] заблокировал бота')
                        bot_blockers.append(recipient.user_id)

                    except Exception as err:
                        logger.error(f'[{recipient.user_id}] {err}')
                    else:
                        logger.info(f'[{recipient.user_id}] успешно отправил анкету {profile.user_id}')
                        await db.functions.add_to_viewed(recipient.user_id, profile.user_id)

                    await asyncio.sleep(1)
