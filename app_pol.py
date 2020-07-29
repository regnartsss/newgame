from aiogram import executor
# from handlers import dp
from utils.start_all import all
from data.config import admins
from loader import dp, bot, storage


async def on_startup(dp):
    #import filters
    import middlewares
    # filters.setup(dp)
    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await all()


async def on_shutdown():
    await bot.send_message(admins, "Бот остановлен")
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    import handlers
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
