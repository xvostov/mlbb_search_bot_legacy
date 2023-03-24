from loader import dp
from .middlewares import *


dp.middleware.setup(UserBlockMiddleware())