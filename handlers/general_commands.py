from aiogram import types
from loader import dp
from work.Users import search_user, db
from utils import sql
import work
# from middleware.middleware_and_antiflood import rate_limit

# logging.basicConfig(level=logging.INFO)

# class MyFilter(BoundFilter):
#     key = 'is_admin'
#     def __init__(self, is_admin):
#        self.is_admin = is_admin
#     async def check(self, message: types.Message):
#         member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#         return member.is_chat_admin()
#
# dp.filters_factory.bind(MyFilter)
#
# @dp.message_handler(is_admin=True, commands=['update'])
# async def admin(message: types.Message):
#     await message.answer("ты админ")
# @dp.message_handler(is_superuser=True, commands='restart')
# async def restart(message: types.Message):
#     def tread_stop(sec=1):
#         import time
#         time.sleep(sec)
#         # noinspection PyProtectedMember
#         os._exit(1)
#     msg = f"Exited by superuser {message.from_user.id} command /restart"
#     logger.warning(msg)
#     import threading
#     threading.Thread(target=tread_stop, args=()).start()
#
@dp.message_handler(commands=['sql'])
# @rate_limit(5, 'start')
async def cmd_start(message: types.Message):
    print(message.text[5:])
    request = message.text[5:]
    await sql.sql_insert(request)
    # if (await sql.sql_selectone("select start_bot from data"))[0] == 1:
    #     print("Бот остановлен")
    #     await message.answer("Бот временно остановлен")
    # else:
    #     if message.text.split(" ")[0] == "/start":
    #         await search_user(message)


@dp.message_handler(commands=['start'])
# @rate_limit(5, 'start')
async def cmd_start(message: types.Message):
    if (await sql.sql_selectone("select start_bot from data"))[0] == 1:
        print("Бот остановлен")
        await message.answer("Бот временно остановлен")
    else:
        if message.text.split(" ")[0] == "/start":
            await search_user(message)


@dp.message_handler(commands=["referrals"])
async def check_referrals(message: types.Message):
    if await sql.sql_selectone("select start_bot from data")[0] == 1:
        print("Бот остановлен")
        await message.answer("Бот временно остановлен")
    else:
        referrals = await db.check_referrals()
        text = f"Ваши рефералы:{referrals}"
        await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["stopbot"])
async def stopbot(message: types.Message):
    if message.chat.id in work.admin_id:
        await sql.sql_insert("Update data Set start_bot = 1")
        await message.answer("Бот остановлен")
    else:
        await message.answer("Ты не админ")


@dp.message_handler(commands=["startbot"])
async def stopbot(message: types.Message):
    if message.chat.id in work.admin_id:
        await sql.sql_insert("Update data Set start_bot = 0")
        await message.answer("Бот запущен")
    else:
        await message.answer("Ты не админ")


@dp.message_handler(commands=["reload"])
async def stopbot(message: types.Message):
    if message.chat.id in work.admin_id:

        await message.answer("Модули перезапущены")
    else:
        await message.answer("Ты не админ")




# await message.answer("Обработчик команды /start")

# # try:
# #     if resource[str(message.chat.id)]["start"] == 1:
# #         if message.text == texting.button_mining_map:
# #             resource[str(message.chat.id)]["start"] = 0
# #         else:
# #             bot.send_message(text="Вы заняты добычей", chat_id=message.chat.id)
# #             return
# # except:
# #     pass
# # if message.chat.id == ADMIN:
# #     #        bot.send_message(text="Админское меню", chat_id=message.chat.id, reply_markup=texting.keyadmin())
# #     pass

# game_new.new_user(message)
# elif message.text == "/button":
#     resource[str(message.chat.id)]["start"] = 0
#     save("resource")
#     bot.send_message(text="Кнопки", chat_id=message.chat.id, reply_markup=keyboard.keyboard_main_menu())
# # elif message.text == "/shop":
# #     bot.send_message(chat_id=message.chat.id, text="Для подробной информации о товаре, нажмите на него",
# #                      reply_markup=Shop(message=message).keyboard_shop())
