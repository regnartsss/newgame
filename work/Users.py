from utils import sql
from text import texting
from keyboards import keyboard
import random
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime
from aiogram import types
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError
from loader import bot
import database
import asyncio


class NewName(StatesGroup):
    name = State()
    us = State()


class DB_USER:
    ADD_NEW_USER_REFERRAL = f"""INSERT INTO heroes(user_id, 'username', 'data', 'avatar', 'nik_name',referral) 
VALUES (%s, '%s', '%s', '%s', '%s', %s)"""
    ADD_NEW_USER = "INSERT INTO heroes(user_id, username, data, avatar, nik_name) VALUES (%s, '%s', '%s', '%s', '%s')"
    COUNT_USERS = "SELECT COUNT(*) FROM heroes"
    # GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT user_id FROM heroes WHERE referral = %s"

    # ADD_NEW_USER_RESOURCE =
    # CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    # ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"
    ADD_NEW_USER_WARRIOR = "INSERT INTO warrior VALUES (%s, %s,0,0,0)"

    async def add_new_user(self, referral=None):

        user = types.User.get_current()
        user_id = user.id
        username = user.username
        nik_name = "player_%i" % (random.randint(1, 9999999))
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        avatar = "👶"
        farm_time = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        args = user_id, username, data, avatar, nik_name

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            print("нет реферала")
            command = self.ADD_NEW_USER
        # print(self.ADD_NEW_USER_RESOURCE)
        request = f"""INSERT INTO resource (user_id, farm_timer) 
VALUES ({user_id}, strftime('%Y:%m:%d:%H:%M:%S','now','localtime'))"""
        #                   INSERT INTO warrior VALUES ({user_id}, 1,0,0,0);
        # INSERT INTO warrior VALUES ({user_id}, 2,0,0,0);
        # INSERT INTO warrior VALUES ({user_id}, 3,0,0,0);
        # INSERT INTO warrior VALUES ({user_id}, 4,0,0,0);
        # INSERT INTO warrior VALUES ({user_id}, 5,0,0,0);"""
        await sql.sql_insert(request)
        await self.warrior_user()
        try:
            record_id = await sql.sql_insert(command % args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await sql.sql_selectone(self.COUNT_USERS)
        return record

    async def warrior_user(self):
        i = 1
        # print("fffff")
        user_id = types.User.get_current().id
        command = self.ADD_NEW_USER_WARRIOR

        while i <= 5:
            await sql.sql_insert(command % (user_id, i))
            i += 1

    async def check_referrals(self):
        user_id = types.User.get_current().id
        command = self.CHECK_REFERRALS
        # print(command % user_id)
        rows = await sql.sql_select(command % user_id)
        #        for num, user in enumerate(rows):
        #             print((await bot.get_chat(user[0])).get_mention(as_html=True))
        return ", ".join([
            f"\n{num + 1}. " + (await bot.get_chat(user[0])).get_mention(as_html=True)
            for num, user in enumerate(rows)
        ])


db = DB_USER()


async def start_user_name(message):
    print("test")
    if not message.from_user.username:
        button = "player_%i" % (random.randint(1, 9999999))
    else:
        button = ReplyKeyboardMarkup(resize_keyboard=True).row(message.from_user.username)
    await NewName.name.set()
    await message.answer(text=texting.text_user_name, reply_markup=button)


async def search_user(message):
    user = (await sql.sql_selectone("select count(user_id) from heroes where user_id = %s" % message.chat.id))[0]
    if user == 1:
        print("Пользователь есть")
        await message.answer(text=texting.text_user_is, reply_markup=keyboard.keyboard_main_menu())
    else:
        await register_user(message)
        await message.answer(text=texting.text_start, reply_markup=keyboard.keyboard_start())


async def register_user(message):
    text = ""
    user_id = message.chat.id
    referral = message.get_args()
    # nik_name = "player_%i" % (random.randint(1, 9999999))
    # username = message.from_user.username
    # data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # avatar = "👶"
    # farm_time = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    await db.add_new_user(referral=referral)
    count_users = await db.count_users()
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={user_id}"
    # balance = await db.check_balance()
    text += f"""
            Сейчас в базе {count_users} человек!
    Ваша реферальная ссылка: {bot_link}
    Проверить рефералов можно по команде: /referrals
            """
    # print(text)
    # print(farm_time)
    # sql.sql_insert("INSERT INTO heroes VALUES (%s,'%s','%s','%s','%s', 0,2,0,2,1,0,1,50,0,0,'%s',0,0,0,0,0,0,0,0)" % (
    #     user_id, username, data, avatar, nik_name, referral))

    # sql.sql_insert("INSERT INTO building VALUES (%s, 1,0,0,0,0,0,0)" % user_id)
    await start_cell(message)
    await start_parameters(user_id=user_id)
    await message.answer(text)


# Новый пользователь - разместить на карте
async def start_cell(message):
    count = (await sql.sql_selectone("select count (*) from maps"))[0]
    r = random.randint(1, count)
    if (await sql.sql_selectone("SELECT resource FROM maps WHERE maps_id=%s" % r))[0] == "null":
        await sql.sql_insert(
            "Update maps set maps_id =%s, resource = 'user', id = %s WHERE maps_id = %s" % (r, message.chat.id, r))
        await sql.sql_insert("UPDATE heroes SET cell = '%s' WHERE user_id = %s" % (r, message.chat.id))
    else:
        await start_cell(message)


async def start_user_default():
    rows = await sql.sql_select("select user_id, lvlheroes, lvlstep from heroes")
    for row in rows:
        await start_parameters(row[0])


async def start_parameters(user_id=None):
    request = f"""Update heroes SET 
    health_used = (SELECT health FROM heroes LEFT JOIN data_heroes 
ON heroes.lvlheroes = data_heroes.lvlheroes WHERE user_id = {user_id}),
    energy_used = (SELECT energy FROM heroes LEFT JOIN data_heroes 
ON heroes.lvlheroes = data_heroes.lvlheroes WHERE user_id = {user_id}),
    step_used = (SELECT step FROM heroes LEFT JOIN data_step 
ON heroes.lvlstep = data_step.lvlstep WHERE user_id = {user_id})
    WHERE user_id =  {user_id}"""
    await sql.sql_insertscript(request)


# Вывод инфы о герое
async def info_heroes(message, key=None):
    user_id = message.chat.id
    request_one = f"""SELECT 
avatar, nik_name,energy_used, step_used, heroes.lvlstep, wolk_used, heroes.lvlheroes, health_used, experience_used,
heroes.cell, wood, stone, iron, food, gold, diamond, energy, experience, health, wolk, step, hit
FROM  heroes, resource 
LEFT JOIN data_heroes ON heroes.lvlheroes = data_heroes.lvlheroes
LEFT JOIN data_step ON heroes.lvlstep = data_step.lvlstep
WHERE heroes.user_id = {user_id} AND resource.user_id = {user_id}"""
    # print(request_one)
    row = await sql.sql_selectone(request_one)
    # print(row)
    avatar = row[0]
    nikname = row[1]
    energy_used = row[2]
    step_used = row[3]
    lvlstep = row[4]
    wolk_used = row[5]
    level = row[6]
    health_used = row[7]
    experience_used = row[8]
    cell = row[9]
    energy = row[16]
    experience = row[17]
    health = row[18]
    hit = row[21]
    wolk = row[19]
    step = row[20]
    wood = row[10]
    stone = row[11]
    iron = row[12]
    food = row[13]
    gold = row[14]
    diamond = row[15]
    coord = await coordinates(cell)
    info_hero = texting.text_info_heroes % (
        avatar, user_id, nikname, coord, level, energy_used, energy, experience_used, experience, health_used, health,
        hit,
        lvlstep, wolk_used, wolk, step_used, step, gold, diamond)
    stat = texting.text_info_storage % (stone, wood, iron, food, gold)
    if key == "heroes":
        return info_hero
    elif key == "build":
        return stat
    else:
        await message.answer(f"{info_hero}\n{stat}")


# Координаты героя
async def coordinates(cell):
    x = int(cell / 100)
    y = cell - x * 100
    return "%s:%s" % (x, y)


# async def update_statistic(user_id):
#     # print(user_id)
#     pass
#     # if data == "step":
#
#
# #         if users[str(message.chat.id)]["wolk_used"] >= step[users[str(message.chat.id)]["lvlstep"]]["wolk"]:
# #             users[str(message.chat.id)]["lvlstep"] += 1
# #             users[str(message.chat.id)]["wolk_used"] = 0
# #         else:
# #             pass
# #     elif data == "experience":
# #         if users[str(message.chat.id)]["experience_used"] >= heroes[users[str(message.chat.id)]["lvlheroes"]][
# #             "experience"]:
# #             users[str(message.chat.id)]["lvlheroes"] += 1
# #             users[str(message.chat.id)]["experience_used"] = 0
# #             users[str(message.chat.id)]["health_used"] = heroes[users[str(message.chat.id)]["lvlheroes"]]["health"]
# #             users[str(message.chat.id)]["energy_used"] = heroes[users[str(message.chat.id)]["lvlheroes"]]["energy"]
# #             chat = int(hero[str(message.chat.id)]["ref"])
# #             if chat != "0":
# #                 bot.send_message(chat_id=chat, text=texting.text_ref_up % users[str(message.chat.id)]["lvlheroes"])
# #                 resource[str(chat)]["diamond"] += users[str(message.chat.id)]["lvlheroes"]
# #         else:
# #             pass
# #     save("users")


# Подсчет шагов
async def recovery_move(message):
    user_id = message.chat.id
    step, step_used, wolk, wolk_used = await sql.sql_selectone(f"""SELECT step, step_used, wolk, wolk_used 
FROM heroes LEFT JOIN data_step 
ON heroes.lvlstep = data_step.lvlstep 
WHERE user_id = {user_id}""")
    if step_used >= step:
        print("Включить таймер")
        await sql.sql_insert(
            f"UPDATE heroes SET step_used = step_used - 1, wolk_used = wolk_used + 1 WHERE user_id = {user_id}")
        # threading.Thread(target=timer_step, args=(step, user_id,)).start()
        # await
        asyncio.ensure_future(timer_step(step, user_id))
    elif step_used == 0:
        print("Ходы кончились")
    elif step_used < step:
        await sql.sql_insert(
            f"UPDATE heroes SET step_used = step_used - 1, wolk_used = wolk_used + 1 WHERE user_id = {user_id}")
    if wolk_used >= wolk:
        await sql.sql_insert(f"UPDATE heroes SET lvlstep = lvlstep + 1, wolk_used = 0 WHERE user_id = {user_id}")


# Восстановление шагов
async def timer_step(step, user_id):
    print("старт шагов")
    while (await sql.sql_selectone("SELECT step_used FROM heroes WHERE user_id = %s" % user_id))[0] < step:
        await asyncio.sleep(database.time_step)  # in seconds
        await sql.sql_insert(f"UPDATE heroes SET step_used = step_used + 1 WHERE user_id = %s" % user_id)


# new Восстановление энергии
async def timer_energy(energy, user_id):
    print("старт энергия")
    while (await sql.sql_selectone(f"SELECT energy_used FROM heroes WHERE user_id = {user_id}"))[0] < energy:
        print("start energy")
        await asyncio.sleep(database.time_energy)  # in seconds
        await sql.sql_insert(f"UPDATE heroes SET energy_used = energy_used + 1 WHERE user_id = {user_id}")


# new Подсчет энергии
async def recovery_energy(message):
    user_id = message.chat.id
    request = f"""SELECT energy, energy_used, experience, experience_used
        FROM heroes LEFT JOIN data_heroes
        ON heroes.lvlheroes = data_heroes.lvlheroes
        WHERE user_id = {user_id}"""
    energy, energy_used, experience, experience_used = await sql.sql_selectone(request)
    if energy_used >= energy:
        await sql.sql_insert(f"UPDATE heroes SET energy_used = energy_used - 1 WHERE user_id = {user_id}")
        # threading.Thread(target=timer_energy, args=(energy, user_id,)).start()
        asyncio.ensure_future(timer_energy(energy, user_id))
    elif energy_used == 0:
        print("Энергия кончилась")
    elif energy_used < energy:
        await sql.sql_insert(f"UPDATE heroes SET energy_used = energy_used - 1 WHERE user_id = {user_id}")
    if experience_used >= experience:
        print("Новый лвл")
        await sql.sql_insert(
            f"""UPDATE heroes SET lvlheroes = lvlheroes + 1, experience_used = experience_used - {experience} 
WHERE user_id = {user_id}""")
        lvl, referral = await sql.sql_selectone(f"SELECT lvlheroes, referral FROM heroes WHERE user_id = {user_id}")
        request = f"UPDATE resource SET diamond = diamond + {int(lvl) * 5} WHERE user_id = {referral}"
        print(request)
        await sql.sql_selectone(request)
        await bot.send_message(chat_id=referral, text=f"Вам начисленны {int(lvl) * 5} алмазов за вашего реферала")
        # await update_statistic(user_id)
        await start_parameters(user_id)


async def recovery_health(message):
    user_id = message.chat.id
    request = f"""SELECT health, health_used
         FROM heroes LEFT JOIN data_heroes
         ON heroes.lvlheroes = data_heroes.lvlheroes
         WHERE user_id = {user_id}"""
    health, health_used = await sql.sql_selectone(request)
    if health_used < health:
        asyncio.ensure_future(timer_health(health, user_id))
    else:
        print("Здоровье кончилось")


async def timer_health(health, user_id):
    while (await sql.sql_selectone(f"SELECT health_used FROM heroes WHERE user_id = {user_id}"))[0] < health:
        print("start health")
        await asyncio.sleep(database.time_healts)  # in seconds
        await sql.sql_insert(f"UPDATE heroes SET health_used = {health} WHERE user_id = {user_id}")
