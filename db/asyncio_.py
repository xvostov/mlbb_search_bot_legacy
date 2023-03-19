from sqlalchemy.ext.asyncio import async_sessionmaker
from settings import DB_PASSWORD, DB_PORT, DB_NAME, DB_HOST
from sqlalchemy.ext.asyncio import create_async_engine

ASYNC_DB_ENGINE = create_async_engine(f'mysql+asyncmy://root:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
session_maker = async_sessionmaker(bind=ASYNC_DB_ENGINE, expire_on_commit=False)