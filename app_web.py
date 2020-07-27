from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from data.config import API_TOKEN, PROXY_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher
import logging
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import ssl
import os
def find_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).replace('\\', '/') + '/'


PATH = find_location()

# webhook settings
WEBHOOK_HOST = 'https://www.heroeslife.online'
WEBHOOK_PATH = ''
WEBHOOK_PORT = 8443
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBHOOK_SSL_CERT = PATH+'/certificate.crt'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = PATH+'/certificate_priv.crt'  # Path to the ssl private key
# webserver settings
WEBAPP_HOST = '10.0.111.111'  # or ip
WEBAPP_PORT = 8443
logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# PROXY_AUTH = aiohttp.BasicAuth(login='SsBNpW', password='oTUn9X')
#bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
storage = RedisStorage2(db=5)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

@dp.message_handler()
async def echo(message: types.Message):
    print("fffff")
    # Regular request
    # await bot.send_message(message.chat.id, message.text)
    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    print(WEBHOOK_URL)
    await bot.send_message(765333440, text="Запущен")
    # await bot.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'r'))
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=ssl_context
    )

