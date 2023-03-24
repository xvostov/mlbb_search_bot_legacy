from aiogram.types import Message
from .models import User


def create_user(message: Message) -> User:
    user = User(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        has_tg_premium=False if message.from_user.is_premium is None else True,
    )

    return user
