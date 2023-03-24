from aiogram import executor
from loader import dp, loop
from postman import distribution_iteration

# Загружаем файл с регистрацией обработчиков и middlewares
import handlers
import middlewares



if __name__ == '__main__':
    loop.create_task(distribution_iteration())
    executor.start_polling(dp, skip_updates=True)
