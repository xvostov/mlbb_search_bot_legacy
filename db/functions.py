from sqlalchemy import select, delete
from .base import *
from .models import User, Profile, View, UserFilter

async def add_user(user: User):
    await add_to_db(user)


async def get_user_by_id(user_id: int) -> User:
    query = select(User).filter_by(user_id=user_id)
    return await select_one(query)


async def add_profile_to_db(profile: Profile):
    await add_to_db(profile)

async def get_profile_by_user_id(user_id):
    query = select(Profile).filter_by(user_id=user_id)
    return await select_one(query)

async def delete_profile_by_user_id(user_id):
    query = delete(Profile).filter_by(user_id=user_id)
    await execute_(query)


async def get_all_profiles():
    query = select(Profile)
    return await select_(query)

async def get_all_users():
    query = select(User)
    return await select_(query)

async def add_to_viewed(view: View):
    await add_to_db(view)


async def add_filter_to_db(user_filter: UserFilter):
    await add_to_db(user_filter)


async def delete_filter_by_user_id(user_id):
    query = delete(UserFilter).filter_by(user_id=user_id)
    await execute_(query)

async def get_filter_by_user_id(user_id):
    query = select(UserFilter).filter_by(user_id=user_id)
    return await select_one(query)


async def get_view_of_profile(user_id):
    query = select(View).filter_by(observer_user_id=user_id)
    return await select_(query)

