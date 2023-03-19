from .asyncio_ import ASYNC_DB_ENGINE as engine
from .models import BaseModel
import asyncio

async def create_all():
    async with engine.begin() as connect:
        await connect.run_sync(BaseModel.metadata.create_all)


loop = asyncio.get_event_loop()
loop.create_task(create_all())
