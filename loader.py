import asyncio

from settings import BOT_TOKEN, PROM_EXP_PORT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from prometheus_client import start_http_server, Counter




start_http_server(PROM_EXP_PORT)

# aiogram
storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

# Metrics
start_cmd_counter = Counter('start_cmd_counter', 'Считает нажатие start при условии, что у человека нет анкеты')
start_profile_creation = Counter('start_profile_creation', 'Считает количество  введения команды new_profile при условии,'
                                                           ' что у человека нет анкеты')
successful_profile_creation = Counter('successful_profile_creation', 'Считает количество успешно созданных анкет')
successful_profile_deletion = Counter('successful_profile_deletion', 'Считает количество успешно удаленных анкет')