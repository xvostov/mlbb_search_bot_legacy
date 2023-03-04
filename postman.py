import asyncio

import db.functions
from loader import bot
from keyboards.inline import get_like_dislike_kb
from utils import render_msg
from loguru import logger

async def send_notification(recipient, profile):
    kb = await get_like_dislike_kb(recipient.user_id, profile.user_id)
    await bot.send_message(recipient.user_id, render_msg(profile),
                           reply_markup=kb)

async def distribution_iteration():
    while True:
        profiles = await db.functions.get_all_profiles()

        for profile in profiles:
            for recipient in profiles:
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

                    except Exception as err:
                        logger.error(err)
                    else:
                        logger.info(f'[{recipient.user_id}] успешно отправил анкету {profile.user_id}')
                        await db.functions.add_to_viewed(recipient.user_id, profile.user_id)

                    await asyncio.sleep(1)
