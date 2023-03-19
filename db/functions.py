from sqlalchemy import select, delete
from .models import User, Profile, View, UserFilter
from .asyncio_ import session_maker
from .utils import get_attr_string
from loguru import logger

async def add_to_db(obj):
    logger.debug(f'Добавляю в базу объект: {get_attr_string(obj)}')
    async with session_maker() as session:
        async with session.begin():
            session.add(obj)

async def select_(query):
    logger.debug(f'Выполняю select: {query}')
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(query)
            return result
async def select_one(query):
    result = await select_(query)
    result = result.first()
    if result is None:
        return None
    else:
        return result[0]

async def execute_(query):
    logger.debug(f'Выполняю execute: {query}')
    async with session_maker() as session:
        async with session.begin():
            await session.execute(query)


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


async def add_to_viewed(view: View):
    await add_to_db(view)


async def add_filter_to_db(user_filter: UserFilter):
    await add_to_db(user_filter)


async def delete_filter_by_user_id(user_id):
    query = delete(UserFilter).filter_by(user_id=user_id)
    await execute_(query)

async def get_filter_by_user_id(user_id):
    query = select(UserFilter).filter_by(user_id=user_id)
    await select_one(query)

