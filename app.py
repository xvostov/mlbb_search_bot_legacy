from aiogram import executor
# from handlers.profile import register_client_handlers
from loader import dp, loop
from postman import distribution_iteration
import handlers


if __name__ == '__main__':
    loop.create_task(distribution_iteration())
    executor.start_polling(dp, skip_updates=True)