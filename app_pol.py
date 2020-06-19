from aiogram import executor
from handlers import dp
from utils.start_all import all
from data.config import admins
import asyncio
# # from middleware.middleware_and_antiflood import ThrottlingMiddleware
#
#

# # asyncio.run(all())
# if __name__ == "__main__":
#     # dp.middleware.setup(ThrottlingMiddleware())
#     executor.start_polling(dp, on_startup=on_startup)
#
#
# #
from loader import bot, storage
# #
#
async def on_startup(dp):
    # import filters
    import middlewares
    # filters.setup(dp)
    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await all()


async def on_shutdown(dp):
    # await bot.send_message(admins, "Бот остановлен")
    await bot.close()
    await storage.close()


# asyncio.run(all())
# async def startbot():

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)




