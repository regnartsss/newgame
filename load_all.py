import logging
from aiogram import Bot, Dispatcher
import aiohttp
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import aioredis

API_TOKEN = '887257503:AAGYnE_ReTm9HzkN047WXgrx2Wh9GKqHYQ8'
PROXY_URL = 'socks5://194.242.126.235:8000'
PROXY_AUTH = aiohttp.BasicAuth(login='SsBNpW', password='oTUn9X')
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# In this example Redis storage is used

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
storage = MemoryStorage()
# storage = RedisStorage2(db=5)
dp = Dispatcher(bot, storage=storage)





def benchmark(func):
    global st

    def wrapper(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time() - t)
        return res
    return wrapper