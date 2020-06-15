import random
from utils import sql
import sqlite3
from text import texting
from keyboards import keyboard
import time
from loader import dp, bot
from aiogram import types
from datetime import datetime, timedelta
from work.Users import recovery_move
from work.BattleCastle import castle_st
import asyncio

async def goto(call, message):
    pole = 100
    print(message.text)
    if message.text in texting.list_Maps_goto or message.text[:3] == "/--" or message.text == "Ходите":
        await message.answer(text=texting.text_goto_maps, reply_markup=await keyboard_map(message))
    else:
        if call.data == " ":
            try:
                await bot.answer_callback_query(callback_query_id=call.id, text='!')
            except Exception as n:
                print(n)
        else:
            row = await sql.sql_selectone(f"select cell, step_used, health_used "
                                          f"from heroes where user_id = {message.chat.id}")
            cell_user = row[0]
            step_used = row[1]
            health_used = row[2]
            value_call = (await sql.sql_selectone(f"SELECT resource FROM maps WHERE maps_id={call.data}"))[0]
            if step_used <= 0:
                await bot.answer_callback_query(callback_query_id=call.id, text='У вас нет ходов')
            elif health_used <= 0:
                await bot.answer_callback_query(callback_query_id=call.id, text='Вы мертвы')
            elif call.data == str(cell_user):
                await bot.answer_callback_query(callback_query_id=call.id, text='Это вы')
            elif int(call.data) == int(cell_user) - 1:
                await database(message, call, cell_user, value_call, -1)
            elif int(call.data) == int(cell_user) + 1:
                await database(message, call, cell_user, value_call, +1)
            elif int(call.data) == int(cell_user) - pole:
                await database(message, call, cell_user, value_call, - pole)
            elif int(call.data) == int(cell_user) + pole:
                await database(message, call, cell_user, value_call, + pole)
            elif value_call == "null":
                await bot.answer_callback_query(callback_query_id=call.id, text='Поле не активно')
            elif value_call == "iron":
                await bot.answer_callback_query(callback_query_id=call.id, text='Шахта с железои')
            elif value_call == "wood":
                await bot.answer_callback_query(callback_query_id=call.id, text='Шахта с деревом')
            elif value_call == "stone":
                await bot.answer_callback_query(callback_query_id=call.id, text='Шахта с камнем')
            elif value_call == "enemy":
                await bot.answer_callback_query(callback_query_id=call.id, text='Страшный монстр')
            elif value_call == "user":
                await bot.answer_callback_query(callback_query_id=call.id, text='Город соперника')


async def keyboard_map(message):
    keyboard_pole = types.InlineKeyboardMarkup()
    x, y, cell_user, n, pole = 1, 0, "", 0, 100
    cell_user = (await sql.sql_selectone(f"select cell from heroes where user_id = {message.chat.id}"))[0]
    if (int(cell_user) % pole) == 3:
        pos = [pole * 3 + 2, pole * 2 + 2, pole + 2, 2, (pole - 2) * -1, (pole * 2 - 2) * -1,
               (pole * 3 - 2) * -1]
    elif int(cell_user) % pole == 2:
        pos = [pole * 3 + 1, pole * 2 + 1, pole + 1, 1, (pole - 1) * -1, (pole * 2 - 1) * -1,
               (pole * 3 - 1) * -1]
    elif int(cell_user) % pole == 1:
        pos = [pole * 3, pole * 2, pole, 0, pole * -1, pole * -2, pole * -3]
    else:
        pos = [pole * 3 + 3, pole * 2 + 3, pole + 3, 3, (pole - 3) * -1, (pole * 2 - 3) * -1,
               (pole * 3 - 3) * -1]
    test = ""
    for x in pos:

        start_field = int(cell_user) - x
        test += f"""SELECT resource, maps_id, id  FROM maps WHERE maps_id BETWEEN {start_field} and {start_field+6} 
UNION ALL \n"""
        # print(test)
        # request = f"SELECT resource FROM maps WHERE {minimum} < maps_id < {maximum}"
    # print(await sql.sql_select(request))
    test = test[:-11] + "ORDER BY maps_id"
    rows = await sql.sql_select(test)
    # print(rows)
    # print(rows[3][0])
    i = 0
    # for row in rows:
    # for x in pos:
    x = 0
    while x < 7:
        try:
            start_field = rows[i][1]
        except IndexError:
            break
        else:
            if start_field < 0:
                continue
        tab = []
        y = 0
        # if (start_field + 7) % pole == 1 or (start_field + 7) % pole == 2 or (start_field + 7) % pole == 3:
        #     start_field = start_field - (start_field + 6) % pole
        while y < 7:
            cell_r = rows[i][0]
            # cell_r = await sql.sql_selectone("SELECT resource FROM maps WHERE maps_id=%s" % start_field)[0]
            # if cell_r == "user":
            #     cell_r = await sql.sql_selectone("SELECT id FROM maps WHERE maps_id=%s" % start_field)[0]
            if start_field % pole == 0 or start_field % pole == 100:
                y = 7
                tab.append(types.InlineKeyboardButton(" ", callback_data=f"{rows[i][1]}"))
            else:
                # print(start_field)
                # print(cell_r)
                # print(rows[i][1])
                if cell_r == "iron":
                    tab.append(types.InlineKeyboardButton("⚒", callback_data=f"{rows[i][1]}"))
                elif cell_r == "wood":
                    tab.append(types.InlineKeyboardButton("🌲", callback_data=f"{rows[i][1]}"))
                elif cell_r == "stone":
                    tab.append(types.InlineKeyboardButton("⛏", callback_data=f"{rows[i][1]}"))
                elif cell_r == "enemy":
                    tab.append(types.InlineKeyboardButton("👻", callback_data=f"{rows[i][1]}"))
                elif cell_r == str(message.chat.id):
                    avatar = await sql.sql_selectone(f"SELECT avatar FROM heroes WHERE user_id={rows[i][2]}")
                    tab.append(types.InlineKeyboardButton(avatar[0], callback_data=f"{rows[i][1]}"))
                elif cell_r != "null":
                    avatar = await sql.sql_selectone(f"SELECT avatar FROM heroes WHERE user_id={rows[i][2]}")
                    tab.append(types.InlineKeyboardButton(avatar[0], callback_data=f"{rows[i][1]}"))
                elif rows[i][1] == int(cell_user) - 1:
                    tab.append(types.InlineKeyboardButton("⬅", callback_data=f"{rows[i][1]}"))
                elif rows[i][1] == int(cell_user) - pole:
                    tab.append(types.InlineKeyboardButton("⬆", callback_data=f"{rows[i][1]}"))
                elif rows[i][1] == int(cell_user) + 1:
                    tab.append(types.InlineKeyboardButton("➡", callback_data=f"{rows[i][1]}"))
                elif rows[i][1] == int(cell_user) + pole:
                    tab.append(types.InlineKeyboardButton("⬇", callback_data=f"{rows[i][1]}"))
                elif cell_r == "null":
                    tab.append(types.InlineKeyboardButton(" ", callback_data=f"{rows[i][1]}"))
                y += 1
                start_field += 1
            i += 1
        x += 1
        keyboard_pole.row(*tab)
    s, e, h = await sql.sql_selectone(
        f"SELECT step_used, energy_used, health_used FROM heroes WHERE user_id={message.chat.id}")
    step = types.InlineKeyboardButton(text="🚶‍♂️Ходов: %s" % s, callback_data=" ")
    energy = types.InlineKeyboardButton(text="🔋 ️Энергии: %s" % e, callback_data=" ")
    health = types.InlineKeyboardButton(text="❤ Жизнь: %s" % h, callback_data=" ")
    keyboard_pole.row(step, energy, health)
    return keyboard_pole


async def database(message, call, cell_user, value_call, s):
    print(value_call)
    if value_call == "iron" or value_call == "wood" or value_call == "stone":
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as n:
            print(n)
        await mine(message, call.data)
    # enemy
    elif value_call == "enemy":
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as n:
            print(n)
        await enemy_write(message, call.data)
    elif value_call.split("_")[0] == "user":
        # one = int(message.chat.id)
        two = (await sql.sql_selectone(f"SELECT id FROM maps WHERE maps_id = {call.data}"))[0]
        await castle_st(call, two)
    else:
        request = f"""
update heroes set cell = cell + {s} where user_id = {message.chat.id};
update maps set resource = 'null', id = 0 where maps_id = {cell_user};
update maps set resource = 'user', id = {message.chat.id} where maps_id = {int(cell_user) + s};
                         """
        await sql.sql_insertscript(request)
        await recovery_move(message)
        await message.edit_text(text=texting.text_goto, reply_markup=await keyboard_map(message))
        # await bot.edit_message_text(text=texting.text_goto, chat_id=message.chat.id,
        #                       message_id=message.message_id, reply_markup=keyboard_map(message))


# new Запись врага
async def enemy_write(message, cell_r, mess=True):
    print("test")
    request = "Select lvlheroes, energy_used from heroes where user_id = %s" % message.chat.id
    request = await sql.sql_selectone(request)
    r = random.randint(request[0] - 1, request[0])
    if r <= 0:
        r = 1
    request = "select health, hit, avatar from training where name = 'enemy' and lvl = %s" % r
    row_one = await sql.sql_selectone(request)
    request = "insert into battle_enemy values(%s, %s, %s, %s, %s, %s, 0, 0)"
    await sql.sql_insert(request % (message.chat.id, r, row_one[0], 5 * r, cell_r, row_one[1]))
    if mess is True:
        await message.answer(text=texting.text_ataka_enemy % (row_one[2], r, row_one[0]),
                             reply_markup=keyboard.keyboard_battle())


async def mine(message, cell_mining):
    await sql.sql_insert("update heroes set message_id = 0 where user_id = %s" % message.chat.id)
    row = await sql.sql_selectone("select * from maps where maps_id = %s" % cell_mining)
    timer = row[3] // 2
    timer = time_str(timer)
    num = int(row[3]/row[2]+1)
    request = f"""Update resource 
SET resource = '{row[1]}', lvl = {row[2]}, number = {row[3]}, cell = {row[0]}, timer ='{timer}', number_attack ={num} 
Where user_id = {message.chat.id}"""
    await sql.sql_insert(request)
    await message.answer(text=await texting.text_mining(message.chat.id), reply_markup=keyboard.keyboard_keyrudnic())


# Подсчет шагов


async def timer_mining(message, data):
    if data == "start":
        formats = "%Y:%m:%d:%H:%M:%S"
        row = (await sql.sql_selectone("select number from resource where user_id = %s" % message.chat.id))[0]
        seconds = row // 2
        time_s = datetime.now()
        time_s += timedelta(seconds=seconds)
        time_s = time_s.strftime(formats)
        request = """Update resource 
                     SET time_start = strftime('%s','now','localtime'), time_stop = '%s', mining_start = 1 
                     Where user_id = %s"""
        await sql.sql_insert(request % (formats, time_s, message.chat.id))
        await message.answer(text=texting.text_mining_start, reply_markup=keyboard.keyboard_map())
    elif data == "stop":
        row = await sql.sql_selectone(
            "select time_start, resource, cell, mining_start from resource where user_id = %s" % message.chat.id)
        if row[3] == 1:
            farm_time = row[0]
            resource = row[1]
            user_id = message.chat.id
            cell_r = row[2]
            farm_time_old = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            a = farm_time_old.split(':')
            aa = datetime(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]))
            b = farm_time.split(':')
            bb = datetime(int(b[0]), int(b[1]), int(b[2]), int(b[3]), int(b[4]), int(b[5]))
            ss = int((aa - bb).seconds)
            summa = 2 * ss
            request = """
                        Update resource 
                        set %s = %s + %s, production = production + %s, 
                                            time_start = 'null', 
                                            time_stop = 'null', 
                                            mining_start = 0
                        where user_id = %s;
                        Update maps set number = number - %s where maps_id = %s;
                      """ % (resource, resource, summa, summa, user_id, summa, cell_r)
            await sql.sql_insertscript(request)
            text = "⚡️Вы вышли и собрали %s ⚡" % summa
            await message.answer(text=text, reply_markup=keyboard.keyboardmap())
            await goto(call="*", message=message)
        else:
            await message.answer(text="Выход", reply_markup=keyboard.keyboardmap())
            await goto(call="*", message=message)


async def timer_start():
    print("Запуск фарма")
    while True:
        await asyncio.sleep(1)
        request = """select user_id, resource, cell, number from resource 
Where time_stop <= strftime('%Y:%m:%d:%H:%M:%S','now','localtime')"""
        rows = await sql.sql_select(request)
        for row in rows:
            print("Завершено")
            resource = row[1]
            user_id = row[0]
            cell_r = row[2]
            number = row[3]
            request = f"""
                     Update resource
                     set {resource} = {resource} + {number}, production = production + {number},
                                         time_start = 'null',
                                         time_stop = 'null',
                                         mining_start = 0
                     where user_id = {user_id};
                     Update maps set resource = 'null', lvl = 0, number=0, id=0 Where maps_id = {cell_r};
                   """
            await sql.sql_insertscript(request)
            text = f"⚡️Вы завершили добычу ⚡️\nСобрано {number}"
            dp.loop.create_task(send(text, user_id))
            await asyncio.sleep(1)
        await asyncio.sleep(60)


async def send(text, user_id):
    await cell()
    await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard.keyboard_map_castle())


def time_str(timer):
    if timer > 3600:
        return time.strftime('%H:%M:%S', time.gmtime(timer))
    else:
        return time.strftime('%M:%S', time.gmtime(timer))


async def cell():
    n = random.randint(1, 10000)
    if (await sql.sql_selectone("SELECT resource FROM maps WHERE maps_id=%s" % n))[0] == "null":
        resource = await resource_start()
        request = "INSERT INTO maps Values (%s, '%s', %s, %s, 0)" % (n, resource[0], resource[1], resource[2])
        await sql.sql_insert(request)
    else:
        await cell()


async def new_maps():  # Прочитать файл
    pole, n, maps = 100, 0, {}
    all_cell = pole * pole
    await sql.sql_insert("delete from maps")
    rows = await sql.sql_select("select user_id from heroes")
    for row in rows:
        r = random.randint(1, pole * pole)
        if not await sql.sql_select("SELECT id FROM maps WHERE maps_id=%s" % r):
            print("Ячейка пустая")
            await sql.sql_insert("INSERT INTO maps Values (%s, 'user', 0, 0, %s)" % (r, row[0]))
            await sql.sql_insert("UPDATE heroes SET cell = '%s' WHERE user_id = %s" % (r, row[0]))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    while n < all_cell:
        n += 1
        if not await sql.sql_select("SELECT id FROM maps WHERE maps_id=%s" % n):
            resource = await resource_start()
            request = "INSERT INTO maps Values (%s, '%s', %s, %s, 0)" % (n, resource[0], resource[1], resource[2])
            print(request)
            cursor.execute(request)
    conn.commit()
    conn.close()


async def resource_start():
    r = random.randint(1, 20)
    if r == 1:
        return await resource_res(old_res="wood")
    elif r == 2:
        return await resource_res(old_res="stone")
    elif r == 3:
        return await resource_res(old_res="iron")
    elif r == 4:
        return "enemy", 0, 0
    elif r >= 5:
        return "null", 0, 0


async def resource_res(old_res):
    r = random.randint(1, 15)
    if r == 1 or r == 2 or r == 3 or r == 4 or r == 5:
        return old_res, 1, random.randint(3000, 5000)
    elif r == 6 or r == 7 or r == 8 or r == 9:
        return old_res, 2, random.randint(5001, 15000)
    elif r == 10 or r == 11 or r == 12:
        return old_res, 3, random.randint(15001, 30000)
    elif r == 13 or r == 14:
        return old_res, 4, random.randint(30001, 60000)
    elif r == 15:
        return old_res, 5, random.randint(60001, 120000)

#
# def statistics(message):
#     open_maps()
#     w, s, i, u, n, w1, w2, w3, w4, w5, s1, s2, s3, s4, s5, i1, i2, i3, i4, i5,
#     e = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
#     for key, value in maps.items():
#         try:
#             if maps[str(key)]["resource"] == "wood":
#                 if maps[str(key)]["lvl"] == 1:
#                     w1 = w1 + 1
#                 elif maps[str(key)]["lvl"] == 2:
#                     w2 = w2 + 1
#                 elif maps[str(key)]["lvl"] == 3:
#                     w3 = w3 + 1
#                 elif maps[str(key)]["lvl"] == 4:
#                     w4 = w4 + 1
#                 elif maps[str(key)]["lvl"] == 5:
#                     w5 = w5 + 1
#                 w = w + 1
#             elif maps[str(key)]["resource"] == "stone":
#                 if maps[str(key)]["lvl"] == 1:
#                     s1 = s1 + 1
#                 elif maps[str(key)]["lvl"] == 2:
#                     s2 = s2 + 1
#                 elif maps[str(key)]["lvl"] == 3:
#                     s3 = s3 + 1
#                 elif maps[str(key)]["lvl"] == 4:
#                     s4 = s4 + 1
#                 elif maps[str(key)]["lvl"] == 5:
#                     s5 = s5 + 1
#                 s = s + 1
#             elif maps[str(key)]["resource"] == "iron":
#                 if maps[str(key)]["lvl"] == 1:
#                     i1 = i1 + 1
#                 elif maps[str(key)]["lvl"] == 2:
#                     i2 = i2 + 1
#                 elif maps[str(key)]["lvl"] == 3:
#                     i3 = i3 + 1
#                 elif maps[str(key)]["lvl"] == 4:
#                     i4 = i4 + 1
#                 elif maps[str(key)]["lvl"] == 5:
#                     i5 = i5 + 1
#                 i = i + 1
#             elif maps[str(key)]["resource"] == "null":
#                 n = n + 1
#             elif maps[str(key)]["resource"] == "enemy":
#                 e = e + 1
#         except:
#             u = u + 1
#     text = "дерево " + str(w) + " \nlvl 1: " + str(w1) + " \nlvl 2: " + str(w2) + " \nlvl 3: " + str(
#         w3) + " \nlvl 4: " + str(w4) + " \nlvl 5: " + str(w5) \
#            + "\nжелезо " + str(i) + " \nlvl 1: " + str(i1) + " \nlvl 2: " + str(i2) + " \nlvl 3: " + str(
#         i3) + " \nlvl 4: " + str(i4) + " \nlvl 5: " + str(i5) \
#            + "\nкамень " + str(s) + " \nlvl 1: " + str(s1) + " \nlvl 2: " + str(s2) + " \nlvl 3: " + str(
#         s3) + " \nlvl 4: " + str(s4) + " \nlvl 5: " + str(s5) \
#            + "\nигроков " + str(u) + "\nПустых ячеек " + str(n) + "\nВрагов " + str(e)
#     config.bot.send_message(chat_id=message.chat.id, text=text)
