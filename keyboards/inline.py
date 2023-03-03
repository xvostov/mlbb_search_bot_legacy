from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.enums import *
from utils import ranks_levels

__all__ = ['ranks_inline_kb', 'roles_inline_kb', 'yes_no_kb']

ranks_inline_kb = InlineKeyboardMarkup(row_width=3)

[ranks_inline_kb.insert(InlineKeyboardButton(text=rank, callback_data=ranks_levels.get(rank))) for rank in list(ranks_levels.keys())]

roles_inline_kb = InlineKeyboardMarkup(row_width=3)

[roles_inline_kb.insert(InlineKeyboardButton(text=role, callback_data=role.strip())) for role in ROLES.enums]

yes_no_kb = InlineKeyboardMarkup(row_width=2)
yes_no_kb.insert(InlineKeyboardButton(text='Да', callback_data='да'))
yes_no_kb.insert(InlineKeyboardButton(text='Нет', callback_data='нет'))


async def get_like_dislike_kb(user_id, profile_user_id):
    like_dislike_kb = InlineKeyboardMarkup(row_width=2)
    like_dislike_kb.insert(InlineKeyboardButton(text='❤️', callback_data=f'{user_id}:like:{profile_user_id}'))
    like_dislike_kb.insert(InlineKeyboardButton(text='👎', callback_data=f'{user_id}:dislike:{profile_user_id}'))
    return like_dislike_kb

async def get_contact_kb(user_url):
    return InlineKeyboardMarkup().insert(InlineKeyboardButton('Написать', url=user_url))