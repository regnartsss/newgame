from aiogram import Dispatcher
from middlewares.middleware_and_antiflood import ThrottlingMiddleware
from middlewares.delete_messege import DeleteMess
from middlewares.middl_time import TimeTower
from aiogram.contrib.middlewares.logging import LoggingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(DeleteMess())
    dp.middleware.setup(ThrottlingMiddleware(limit=1))
    dp.middleware.setup(TimeTower())
    # dp.middleware.setup(LoggingMiddleware())
    return
