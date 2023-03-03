import asyncio

import aiogram

import db.functions
from loader import bot
from keyboards.inline import get_like_dislike_kb
from utils import render_msg


async def send_notification(recipient, profile):
    await asyncio.sleep(6)
    kb = await get_like_dislike_kb(recipient.user_id, profile.user_id)
    await bot.send_message(recipient.user_id, render_msg(profile),
                           reply_markup=kb)


async def iter_for_profiles(recipient, profiles):
    observered_user_ids = [view.observed_user_id for view in recipient.views]
    for profile in profiles:
        if recipient.user_id == profile.user_id:
            continue

        elif profile.user_id in observered_user_ids:
            continue

        else:
            await db.functions.add_to_viewed(recipient.user_id, profile.user_id)

        try:
            await send_notification(recipient, profile)

        except aiogram.utils.exceptions.BotBlocked:
            pass


async def distribution_iteration():
    while True:
        profiles = await db.functions.get_all_profiles()

        for recipient in profiles:
            if recipient.user_filter:
                recipient_filter = recipient.user_filter
                f_profiles = await db.functions.get_profiles_by_filter(recipient_filter)
                await iter_for_profiles(recipient, f_profiles)

            else:
                await iter_for_profiles(recipient, profiles)

        await asyncio.sleep(20)
