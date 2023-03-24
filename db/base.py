from .asyncio_ import session_maker
from loguru import logger
async def select_(query):
    # logger.debug(f'Выполняю select: {query}')
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]
async def select_one(query):
    result = await select_(query)
    if not result:
        return None
    else:
        return result[0]

async def execute_(query):
    # logger.debug(f'Выполняю execute: {query}')
    async with session_maker() as session:
        async with session.begin():
            await session.execute(query)

async def add_to_db(obj):
    logger.debug(f'Добавляю в базу объект: {obj}')
    async with session_maker() as session:
        async with session.begin():
            session.add(obj)
