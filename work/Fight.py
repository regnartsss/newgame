from text import texting
from aiogram import types
from keyboards.keyboard import keyboard_battle_one_back, keyboardmap, keyboard_main_menu
from loader import bot
from utils import sql
import time
from work.Map import goto, enemy_write
import random
import numpy as np

from work.Users import recovery_energy, recovery_health

import os
def find_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).replace('\\', '/') + '/'

PATH = find_location()
# from Field_resource import field_goto
fight_text, text_ataka = {}, {}
fight_text_all = {"null": " "}


async def keyboard_attaka(user):
    keyboard = types.InlineKeyboardMarkup()
    rows = await sql.sql_select(f"SELECT name, avatar FROM combinations WHERE id > 0 and user_id = {user} ORDER BY id")
    health = (await sql.sql_selectone(f"select health_used from heroes where user_id = {user}"))[0]
    health_enemy = (await sql.sql_selectone(f"select enemy_health from battle_enemy where user_id = {user}"))[0]
    health = types.InlineKeyboardButton(text=f"{health} ❤️", callback_data="1")
    health_enemy = types.InlineKeyboardButton(text=f"{health_enemy} ❤️", callback_data="1")
    x, y = 1, 1
    list_x = [2, 5, 8, 10, 12]
    list_y = [2, 6, 8, 10, 12]
    tab = []
    # keyboard.row(types.InlineKeyboardButton(text="тут текст", callback_data="1"))
    keyboard.row(types.InlineKeyboardButton(text=text_ataka[user]["null"], callback_data="1"))
    for row in rows:
        if x in list_x:
            tab.append(types.InlineKeyboardButton(text="➖➖", callback_data="null"))
        if x == 5:
            tab.append(types.InlineKeyboardButton(text="➖➖", callback_data="null"))
        tab.append(types.InlineKeyboardButton(text=row[1], callback_data="fight_%s" % row[0]))
        if y in list_y:
            keyboard.row(*tab)
            tab = []
        x += 1
        y += 1
    keyboard.row(health, health_enemy)
    return keyboard


async def insert(message):
    user = message.chat.id
    request = f"""
        INSERT INTO "combinations" VALUES(1,'heroes_head',0,'Голова героя','👨','heroes',0,'👨',{user});
        INSERT INTO "combinations" VALUES(3,'heroes_handleft',0,'Левая рука героя','🤛 ','heroes',0,'🤛 ',{user});
        INSERT INTO "combinations" VALUES(4,'heroes_handright',0,'Правая рука героя','🤜','heroes',0,'🤜',{user});
        INSERT INTO "combinations" VALUES(7,'heroes_breast',0,'Тело героя','👕','heroes',0,'👕',{user});
        INSERT INTO "combinations" VALUES(11,'heroes_foot',0,'Обувь героя','👞','heroes',0,'👞',{user});
        INSERT INTO "combinations" VALUES(2,'enemy_head',0,'Голова врага','👨','enemy',0,'👨',{user});
        INSERT INTO "combinations" VALUES(5,'enemy_handleft',0,'Левая рука врага','🤛 ','enemy',0,'🤛 ',{user});
        INSERT INTO "combinations" VALUES(8,'enemy_breast',0,'Тело врага','👕','enemy',0,'👕',{user});
        INSERT INTO "combinations" VALUES(9,'heroes_legs',0,'Ноги героя','👖','heroes',0,'👖',{user});
        INSERT INTO "combinations" VALUES(12,'enemy_foot',0,'Обувь врага','👞','enemy',0,'👞',{user});
        INSERT INTO "combinations" VALUES(10,'enemy_legs',0,'Ноги врага','👖','enemy',0,'👖',{user});
        INSERT INTO "combinations" VALUES(6,'enemy_handright',0,'Правая рука врага','🤜','enemy',0,'🤜',{user});
        UPDATE battle_enemy SET defence = 2, attaka = 2 WHERE user_id = {user}
    """
    await sql.sql_insertscript(request)


async def fight(call, message, mess=False):
    print(message.text)
    user = str(message.chat.id)
    if message.text == texting.button_attack or message.text == "Ходите":
        fight_text[user] = {}
        text_ataka[user] = {}
        text_ataka[user]["round"] = 0
        text_ataka[user]["text"] = "/-------------------------/"
        text_ataka[user]["null"] = "Защита 2 очка. Аттака 2 очка"
        await insert(message)
        if mess is False:
            await message.answer(text="Атака", reply_markup=keyboard_battle_one_back())
            await message.answer(text="Вы атаковали врага. Выберите какую часть тела защитить и атакуйте врага",
                             reply_markup=await keyboard_attaka(user))
        else:
            await message.edit_text(text="Вы атаковали врага. Выберите какую часть тела защитить и атакуйте врага",
                             reply_markup=await keyboard_attaka(user))
    elif message.text == texting.button_goto:
        # combat[user] = {}
        text_ataka[user] = {}

    else:
        data = call.data.split("_")[1]
        data_old = call.data.split("_")[2]
        d = data + "_" + data_old
        row = await sql.sql_selectone("Select defence, attaka from battle_enemy where user_id = %s" % message.chat.id)
        defence = row[0]
        ataka = row[1]
        if data == "heroes":
            if 0 < defence <= 2:
                request = "select avatar from combinations where name = '%s'" % d
                avatar = (await sql.sql_selectone(request))[0]
                request = "Update battle_enemy set defence = defence - 1 where user_id = %s"
                await sql.sql_insert(request % message.chat.id)
                request = f"""Update combinations set number = number + 1 WHERE name = '{d}' and user_id = 123456789;
                              Update combinations set combat = 1, avatar = '{avatar} 🛡' 
                                  where name = '{d}' and user_id = {message.chat.id}"""
                await sql.sql_insertscript(request)

                await bot.answer_callback_query(callback_query_id=call.id, text='Защитились')
            else:
                await bot.answer_callback_query(callback_query_id=call.id, text='Очки защиты законились')
                return
        elif data == "enemy":
            if 0 < ataka <= 2:
                request = f"select avatar from combinations where name = '{d}' and user_id = {message.chat.id}"
                avatar = (await sql.sql_selectone(request))[0]
                request = "Update battle_enemy set attaka = attaka - 1 where user_id = %s"
                await sql.sql_insert(request % message.chat.id)
                request = f"""Update combinations set number = number + 1 WHERE name = '{d}' and user_id = 123456789;
                              Update combinations set combat = 1, avatar = '{avatar} ⚔' 
                                 where name = '{d}' and user_id = {message.chat.id}"""
                await sql.sql_insertscript(request)
                await bot.answer_callback_query(callback_query_id=call.id, text='Атаковали')
            else:
                await bot.answer_callback_query(callback_query_id=call.id, text='Очки атаки законились')
                return
        row = await sql.sql_selectone("Select defence, attaka from battle_enemy where user_id = %s" % message.chat.id)
        defence = row[0]
        ataka = row[1]
        if defence == 0 and ataka == 0:
            await sql.sql_insert("Update battle_enemy set defence = 2, attaka = 2 where user_id = %s" % message.chat.id)
            text_ataka[user]["null"] = "Идет бой, ожидайте"
            await message.edit_text(text=text_ataka[user]["text"], reply_markup=await keyboard_attaka(user))
            print("Бой прошел")
            text_ataka[user]["round"] += 1
            round_num = text_ataka[user]["round"]
            text_ataka[user]["text"] += f"\n/----/ Раунд {round_num} /----/{await combat_battle(message.chat.id)}\n"
            time.sleep(3)
            await sql.sql_insert(f"Update combinations set avatar = avatar_old, combat = 0 where user_id = {user}")
            fight_text[user] = {}
            fight_text[user] = fight_text_all.copy()
            text_ataka[user]["null"] = "Защита 2 очка. Аттака 2 очка"
            health = (await sql.sql_selectone(f"select health_used from heroes where user_id = {user}"))[0]
            health_enemy = (await sql.sql_selectone(f"select enemy_health from battle_enemy where user_id = {user}"))[0]
            print(health_enemy)
            print(health)
            print(max(health_enemy, health))
            # if health_enemy <= 0 and health <= 0:
            #     s = max(health_enemy, health)
            #     # if
            #     print(health_enemy)
            #     print(health)
            #     print(max(health_enemy,health))

            if health_enemy <= 0:
                print("Враг проиграл")
                await message.delete()
                await message.answer(text=text_ataka[user]["text"])
                await congratulation(message, "heroes")
            elif health <= 0:
                print("Герой проиграл")
                await message.delete()
                await message.answer(text=text_ataka[user]["text"])
                await congratulation(message, "enemy")

            #     # if resource[str(self.message_chat_id)]["f_m"] == 1:
            #     #     # congratulation(self.message, "field")
            #     #     self.figth_mining()
            #     #
            #     # else:
            #     #     congratulation(self.message, "heroes")
            #
            else:
                await call.message.edit_text(text=text_ataka[user]["text"], reply_markup=await keyboard_attaka(user))
        else:
            request = "Select defence, attaka from battle_enemy where user_id = %s"
            defence, attaka = await sql.sql_selectone(request % message.chat.id)
            text_ataka[user]["null"] = "Защита %s очка. Аттака %s очка" % (defence, attaka)
            await call.message.edit_text(text=text_ataka[user]["text"], reply_markup=await keyboard_attaka(user))


# async def figth_mining(self):
#     user_mining = resource[str(self.message_chat_id)]["mining"]
#     res = user_mining["resource"]
#     enem_num_resource = user_mining["enem_num_resource"]
#     maps[str(user_mining["cell"])]["number"] -= enem_num_resource
#     if maps[str(user_mining["cell"])]["number"] < 10:
#         maps[str(user_mining["cell"])]["resource"] = "null"
#         maps[str(user_mining["cell"])].pop("lvl")
#         maps[str(user_mining["cell"])].pop("number")
#         cell()
#     resource[str(self.message_chat_id)][res] += enem_num_resource
#     lvl_storage = build[str(self.message_chat_id)]["storage"]
#     if resource[str(self.message_chat_id)][res] > buildings["storage"][lvl_storage]["capacity"]:
#         resource[str(self.message_chat_id)][res] = buildings["storage"][lvl_storage]["capacity"]
#     celli = users[str(self.message_chat_id)]["enemy_cell"]
#     resource[str(self.message_chat_id)]["f_m"] = 0
#     self.field[celli] = 0
#     self.r_print_r("new")


async def combat_battle(user):
    text = " "
    row_max_one = await sql.sql_selectone(
        "SELECT MAX(number), name FROM combinations WHERE data = 'enemy' and user_id = 123456789")
    await sql.sql_insert(f"update combinations SET number = 0 WHERE name = '{row_max_one[1]}' and user_id = {user}")

    row_max_two = await sql.sql_selectone(
        "SELECT MAX(number), name FROM combinations WHERE data = 'enemy' and user_id = 123456789")
    await sql.sql_insert(
        f"update combinations SET number = {row_max_one[0]} WHERE name = '{row_max_one[1]}' and user_id = {user}")

    row_min_one = await sql.sql_selectone(
        "SELECT MIN(number), name FROM combinations WHERE data = 'heroes'and user_id = 123456789")
    await sql.sql_insert(f"update combinations SET number = 99999 WHERE name = '{row_min_one[1]}' and user_id = {user}")

    row_min_two = await sql.sql_selectone(
        "SELECT MIN(number), name FROM combinations WHERE data = 'heroes'and user_id = 123456789")
    await sql.sql_insert(
        f"update combinations SET number = {row_min_one[0]} WHERE name = '{row_min_one[1]}' and user_id = {user}")

    rows = await sql.sql_select(f"SELECT name, description FROM combinations WHERE combat = 1 and user_id = {user}")

    request = f"select enemy_health, enemy_cell, enemy_hit from battle_enemy where user_id = {user}"
    health_enemy, cell, hit_enemy = await sql.sql_selectone(request)
    request = f"""SELECT health, hit FROM heroes INNER JOIN data_heroes ON heroes.lvlheroes = data_heroes.lvlheroes 
                    WHERE user_id = {user}"""
    health, hit = await sql.sql_selectone(request)
    for row in rows:

        if row[0] == row_min_one[1]:
            text += f"\n 🛡 Вы отразили аттаку врага в {row[1]} "
        elif row[0] == row_min_two[1]:
            text += f"\n 🛡 Вы отразили аттаку врага в {row[1]} "
        elif row[0] == row_max_one[1]:
            text += f"\n 🛡 Враг отразил вашу аттаку в {row[1]} "
        elif row[0] == row_max_two[1]:
            text += f"\n 🛡 Враг отразил вашу аттаку в {row[1]} "
        elif row[0].split("_")[0] == 'heroes':
            text += f"\n ⚔️Враг нанес вам удар - {hit_enemy}♥️"
            await sql.sql_insert(f"update heroes SET health_used = health_used - {hit_enemy} WHERE user_id = {user}")
        elif row[0].split("_")[0] == 'enemy':
            text += f"\n ⚔️Вы нанесли удар противнику - {hit} ♥️"
            await sql.sql_insert(f"update battle_enemy SET enemy_health = enemy_health - {hit} WHERE user_id = {user}")
    return text


async def congratulation(message, data):
    if data == "heroes":
        r_gold = random.randint(1, 50)
        cell_r, field = (await sql.sql_selectone(f"""SELECT battle_enemy.enemy_cell, resource.field 
FROM battle_enemy, resource 
WHERE battle_enemy.user_id = {message.chat.id} AND resource.user_id = {message.chat.id}"""))

        text = f"Бой окончен:\n {texting.text_ataka_win % r_gold}"
        await sql.sql_insert(f'delete from battle_enemy where user_id == {message.chat.id}')
        await sql.sql_insert(f'delete from combinations where user_id = {message.chat.id}')
        time.sleep(2)

        # print(field)
        if field == 0:
            request = f"""
                           UPDATE heroes SET experience_used = experience_used + 5 WHERE user_id = {message.chat.id};
                           UPDATE resource SET gold = gold + {r_gold} WHERE user_id = {message.chat.id};
                           UPDATE maps SET resource = 'null', lvl = 0, number=0, id=0 WHERE maps_id = {cell_r};                           
                    """
            await sql.sql_insertscript(request)
            await recovery_energy(message)
            await recovery_health(message)
            await message.answer(text, reply_markup=keyboardmap())
            await goto(message=message, call="  ")
        else:
            text += await mining_attack_win(message.chat.id)
            request = f"""
                           UPDATE heroes SET experience_used = experience_used + 5 WHERE user_id = {message.chat.id};
                           UPDATE resource SET gold = gold + {r_gold}, field = 0 WHERE user_id = {message.chat.id};
                           Update heroes SET 
                            health_used = (SELECT health FROM heroes LEFT JOIN data_heroes 
                            ON heroes.lvlheroes = data_heroes.lvlheroes WHERE user_id = {message.chat.id})
                        """
            await sql.sql_insertscript(request)
            await recovery_energy(message)
            await recovery_health(message)
            await message.answer(text, reply_markup=keyboardmap())
            await field_goto(message)
    elif data == "enemy":
        await sql.sql_insert(f'delete from battle_enemy where user_id == {message.chat.id}')
        await sql.sql_insert(f'delete from combinations where user_id = {message.chat.id}')
        text = f"Бой окончен:\n Вы проиграли"
        await recovery_energy(message)
        await recovery_health(message)
        await message.answer(text, reply_markup=keyboard_main_menu())


async def mining_attack(message):
    await sql.sql_insert(
        f"""update heroes set message_id = {message.message_id} where user_id = {message.chat.id}""")
    lvl = (await sql.sql_selectone(f"SELECT lvl FROM resource WHERE user_id = {message.chat.id}"))[0]
    k = [4, 2.5, 2, 1.75, 1.6]
    h = int(k[lvl - 1] * lvl)
    w = h
    x = 0
    z = np.zeros((w, h))
    y = random.randint(1, w - 1)
    z[x][y] = 2

    async def rand(x, y, z):
        r = random.randint(1, 5)
        if x == h - 1:
            z[x][y] = 4
        elif r == 1 or r == 2:
            try:
                if z[x][y - 1] == 1 or z[x][y - 1] == 2 or y - 1 < 0:
                    await rand(x, y, z)
                else:
                    y -= 1
                    z[x][y] = 1
                    await rand(x, y, z)
            except IndexError:
                pass
        elif r == 3:
            try:
                if z[x + 1][y] == 1:
                    await rand(x, y, z)
                else:
                    x += 1
                    z[x][y] = 1
                    await rand(x, y, z)
            except IndexError:
                pass
        elif r == 4 or r == 5:
            try:
                if z[x][y + 1] == 1 or z[x][y + 1] == 2 or y + 1 > h - 1:
                    await rand(x, y, z)
                else:
                    y += 1
                    z[x][y] = 1
                    await rand(x, y, z)
            except Exception as n:
                print(f"Ошибка {n}")
                await rand(x, y, z)
                pass

    await rand(x, y, z)
    n = np.count_nonzero(z == 1) - 1
    print(n)
    n = int(n / lvl)
    print(n)
    k, x = 0, 0
    while x < h:
        y = 0
        while y < h:
            if z[x][y] == 1:
                if k == n:
                    z[x][y] = 3
                    k = 0
                k += 1
            y += 1
        x += 1

    print(z)
    np.savetxt(PATH+f'temp/{message.chat.id}.txt', z)
    await message.answer(text="Ходите", reply_markup=await keyboard_mining_field(message.chat.id, z))


async def mining_attack_win(user_id):
    row = await sql.sql_selectone(f"select resource, cell, lvl, number, number_attack from resource where user_id = {user_id}")
    request = f"""
UPDATE resource SET {row[0]} = {row[0]} + {row[4]}, production = production + {row[4]} WHERE user_id = {user_id};
UPDATE maps SET number = number - {row[4]} WHERE maps_id = {row[1]};
UPDATE maps SET number = 0, resource = 'null', lvl = 0 WHERE maps_id = {row[1]} and number <= 0;
"""
    print(request)
    await sql.sql_insertscript(request)
    return f"Обыскав врага, вы нашли {row[4]}ед. ресурса"
# r_num = a.count(3)
# resource[str(message.chat.id)]["mining"]["enem_num"] = r_num
# #     resource[str(message.chat.id)]["mining"]["enem"] = r_num
# resource[str(message.chat.id)]["mining"]["enem_num_resource"] = int(
#     resource[str(message.chat.id)]["mining"]["number"] / r_num)
# data_resource = {"wood": "🌲", "stone": "🧱", "iron": "⛓"}
# res = resource[str(message.chat.id)]["mining"]["resource"]
# resource[str(message.chat.id)]["mining"]["avatar"] = data_resource[res]
# field[str(message.chat.id)] = a


async def field_goto(call):
    try:
        a = np.loadtxt(PATH+f'temp/{call.message.chat.id}.txt')
    except:
        a = np.loadtxt(PATH+f'temp/{call.chat.id}.txt')
    result, x, y = 0, 0, 0
    # l = len(a)
    # print(l)
    # i = 0
    # print("her_1")
    # a = len(field) ** 0.5
    #
    # while i <= len(field):
    #     #                print(self.field[i])
    #     if field[i] == 2:
    #         her = i
    #         break
    #     i += 1
    try:
        result = int(call.data.split("_")[1])
        x = int(call.data.split("_")[2])
        y = int(call.data.split("_")[3])
    except AttributeError:
        result = 5
    if result == 0:
        print("не доступно")
        await bot.answer_callback_query(callback_query_id=call.id, text="Ячейка не доступна")
    elif result == 2:
        await bot.answer_callback_query(callback_query_id=call.id, text="Это вы")
    elif result == 1 or result == 3:
        if a[x-1][y] == 2:
            a[x-1][y] = 1
            a[x][y] = 2
        elif a[x+1][y] == 2:
            a[x+1][y] = 1
            a[x][y] = 2
        elif a[x][y-1] == 2:
            a[x][y-1] = 1
            a[x][y] = 2
        elif a[x][y+1] == 2:
            a[x][y+1] = 1
            a[x][y] = 2
            print("rez %s" % result)
            # move(self.message)
        np.savetxt(PATH+f'temp/{call.message.chat.id}.txt', a)
        if result == 1:
            await bot.edit_message_text(text="Ходите", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=await keyboard_mining_field(call.message.chat.id, a))
        elif result == 3:
            cell_r = (await sql.sql_selectone(f"SELECT cell FROM resource WHERE user_id = {call.message.chat.id}"))[0]
            request = f"UPDATE resource SET field = 1 WHERE user_id = {call.message.chat.id}"
            await sql.sql_insert(request)
            await enemy_write(call.message, cell_r, mess=False)
            await fight(message=call.message, call=call, mess=True)
    elif result == 4:
        await call.message.delete()
        await call.message.answer(text="Вы вышли")
        await sql.sql_insert(
            f"""update heroes set message_id = {call.message.chat.id} where user_id = {call.message.chat.id}""")
        # await bot.send_message(text="Вы вышли", chat_id=call.message.chat.id, reply_markup=keyboardmap())
        await goto(message=call.message, call=call)


    elif result == 5:
        await bot.send_message(chat_id=call.chat.id, text="Ходите", reply_markup=await keyboard_mining_field(call.chat.id, a))
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Слишком далеко")
                # print(result)
                # print("атака")
                # users[str(self.message_chat_id)]["defence"] = 2
                # users[str(self.message_chat_id)]["attaka"] = 2
                # print("атака")
                # lvl = users[str(self.message_chat_id)]["lvlheroes"] - 1
                # users[str(self.message_chat_id)]["enemy_lvl"] = lvl
                # users[str(self.message_chat_id)]["enemy_health"] = enemy[lvl]["health"]
                #
                # #                        users[str(self.message_chat_id)]["enemy_exr"] = 5 * lvl
                # users[str(self.message_chat_id)]["enemy_cell"] = cell
                # users[str(self.message_chat_id)]["enemy_hit"] = enemy[lvl]["hit"]
                # resource[str(self.message_chat_id)]["f_m"] = 1
                # print("rrrrrrr")
                # await fight()
    # # await bot.send_message(text = "ghbdtn", chat_id=call.message.chat.id)
    # await call.message.edit_text(text="Ходите", reply_markup=await keyboard_mining_field(call.message.chat.id))



async def keyboard_mining_field(user_id, a):
    keyboard = types.InlineKeyboardMarkup()
    # a = np.loadtxt(f'temp/{user_id}.txt')
    request = f"""SELECT avatar, step_used, energy_used, health_used, resource.resource FROM heroes, resource 
WHERE heroes.user_id = {user_id} and resource.user_id = {user_id}"""
    row = await sql.sql_selectone(request)
    res = {'iron': '⛓', 'stone': '🧱', 'wood': '🌲'}
    dd = {0: res[row[4]], 1: " ", 2: row[0], 3: "👻", 4: "❌"}
    k_k = len(a)
    f = []
    x, y, n = 0, 0, 0
    while x < k_k:
        tab = []
        keyfield = []
        y = 0
        while y < k_k:
            keyfield.append(types.InlineKeyboardButton(text=f"{dd[a[x][y]]}", callback_data=f"field_{int(a[x][y])}_{x}_{y}"))
            y += 1
            n += 1
        x += 1
        f.append(tab)
        keyboard.row(*keyfield)
    step = types.InlineKeyboardButton(text=f"🚶‍♂️Ходов: {row[1]}", callback_data=" ")
    energy = types.InlineKeyboardButton(text=f"🔋 ️Энергии: {row[2]}", callback_data=" ")
    health = types.InlineKeyboardButton(text=f"❤ Здоровье: {row[3]}", callback_data=" ")
    keyboard.row(step, energy, health)
    print(keyboard)
    return keyboard
