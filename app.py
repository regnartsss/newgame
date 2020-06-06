from aiogram import executor
from load_all import dp, bot
from start_all import all
import handlers
from data import admin_id
import asyncio

from  middleware_and_antiflood import ThrottlingMiddleware


async def on_shutdown():
    await bot.close()


async def on_start(gp):
    await bot.send_message(admin_id, "Бот запущен")

asyncio.run(all())
if __name__ == "__main__":
    # from handlers import dp
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True)



