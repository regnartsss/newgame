import random
from loader import bot
# from data import training
import threading
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from text import texting
from keyboards import keyboard
from utils.sql import sql_select, sql_selectone, sql_insert
import asyncio
# def find_location():
#     return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).replace('\\', '/') + '/'
# PATH = find_location()

global castle


async def castle_st(call, two):
    global castle
    user_id = call.message.chat.id
    try:
        castle[f"{user_id}_{two}"] = {}
    except NameError:
        castle = {}
    data = await castle_start(user_id, two)
    try:
        if data[:16] == "У вас нет воинов" or data[:16] == "У соперника нет ":
            await call.message.answer(text=data)
    except Exception as n:
        castle[f"{user_id}_{two}"] = data
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer(text=texting.text_ataka_castle % "nik_name", reply_markup=keyboard.keyboard_castle())
        # await save_castle()


async def castle_start(one, two):
    lvl_castle_one, lvl_castle_two = 0, 0
    request = f"SELECT user_id, castle FROM heroes WHERE user_id = {one} or user_id = {two}"
    rows = await sql_select(request)
    for row in rows:
        if row[0] == one:
            lvl_castle_one = row[1]
        elif row[0] == two:
            lvl_castle_two = row[1]
    if lvl_castle_one >= lvl_castle_two:
        lvl_castle = await castle_start_lvl(lvl_castle_two)
        return await castle_start_queue(one, two, lvl_castle)
    elif lvl_castle_one <= lvl_castle_two:
        lvl_castle = await castle_start_lvl(lvl_castle_one)
        return await castle_start_queue(one, two, lvl_castle)


async def castle_start_lvl(lvl_castle):
    if 0 < lvl_castle <= 4:
        return 1
    elif 4 < lvl_castle <= 8:
        return 2
    elif 8 < lvl_castle <= 12:
        return 3
    elif 12 < lvl_castle <= 16:
        return 4
    elif 16 < lvl_castle <= 20:
        return 5


async def castle_start_queue(one, two, lvl_war):
    warrior = {}
    data = {}
    one_war = await sql_selectone(
        f"SELECT barracks, stable, shooting FROM warrior WHERE user_id = {one} and lvl = {lvl_war}")
    two_war = await sql_selectone(
        f"SELECT barracks, stable, shooting FROM warrior WHERE user_id = {two} and lvl = {lvl_war}")
    warrior[str(one)] = {'barracks': one_war[0], 'stable': one_war[1], 'shooting': one_war[2]}
    warrior[str(two)] = {'barracks': two_war[0], 'stable': two_war[1], 'shooting': two_war[2]}
    stat_one = (sorted(warrior[str(one)].items(), key=lambda k: k[1]))
    stat_two = (sorted(warrior[str(two)].items(), key=lambda k: k[1]))
    queue = {"q": [], "q_one": [], "q_two": []}
    for key in stat_one:
        if key[1] == 0:
            pass
        else:
            queue["q_one"].append(key[0])
    for key in stat_two:
        if key[1] == 0:
            pass
        else:
            queue["q_two"].append(key[0])

    if queue["q_one"] == []:
        return "У вас нет воинов %s уровня" % lvl_war
    if queue["q_two"] == []:
        return "У соперника нет воинов %s уровня" % lvl_war
    i = 0
    while i < 3:
        try:
            queue["q"].append("%s_one" % queue["q_one"][i])
        except:
            pass

        try:
            queue["q"].append("%s_two" % queue["q_two"][i])
        except:
            pass
        i += 1
    queue.pop("q_one")
    queue.pop("q_two")
    data = {"user_one": one, "user_two": two, "lvl_war": str(lvl_war), "start_one": -2, "start_two": -2,
            "chat_id_one": 0, "chat_id_two": 0, "dead_one": 0, "dead_two": 0,
            "goto": " ", "que": 0, "q": queue["q"], "field": [], "t_one": [16, 32, 48], "t_two": [15, 31, 47]}
    return data


class Castle():
    def __init__(self, message, call):
        self.n = 0
        #
        #     #     self.st_one = [0, 8, 16, 24, 32, 40, 48, 56]
        #     #     self.st_two = [7, 15, 23, 31, 39, 47, 55, 63]
        try:
            self.message = message
            self.text = message.text
            self.user_id = message.chat.id
            self.message_id = message.message_id
        except Exception as n:
            print(f"error_1_{n}")
        try:
            self.call = call
            self.call_data = call.data
            self.call_id = call.id
        except Exception as n:
            print(f"error_2_{n}")
        try:
            self.key = self.search_castle()
            self.castle = castle[self.key]
            self.all_castle = castle
        except NameError:
            pass


    def search_castle(self):

        for key, value in castle.items():
            if str(self.user_id) == key.split("_")[0]:
                return key
            elif str(self.user_id) == key.split("_")[1]:
                return key

    async def castle_pole(self, pos=""):
        if self.text == texting.button_castle_attack:
            self.castle["field_one"] = [0 for i in range(0, 64)]
            self.castle["field_two"] = [0 for i in range(0, 64)]
            text_one, text_two = "Вы атаковали замок\n", "Ваш замок атаковали\n"
            keyboard_one, keyboard_two = self.castle_keyboard_start()
            await bot.send_message(chat_id=self.castle["user_one"], text=text_one,
                                   reply_markup=keyboard.keyboard_castle_escape_field())
            await bot.send_message(chat_id=self.castle["user_two"], text=text_two,
                                   reply_markup=keyboard.keyboard_castle_escape_field())
            await bot.send_message(text="----->", chat_id=self.castle["user_one"], reply_markup=keyboard_one)
            await bot.send_message(text="<-----", chat_id=self.castle["user_two"], reply_markup=keyboard_two)
            await self.timer("start")

    async def castle_pole_timer(self):
        if self.user_id == self.castle["user_one"]:
            self.castle["start_one"] = -1
            self.castle["chat_id_one"] = self.message_id
            await self.call.message.edit_text("Ожидайте второго игрока", reply_markup=await self.keyboard_check())
        elif self.user_id == self.castle["user_two"]:
            self.castle["start_two"] = -1
            self.castle["chat_id_two"] = self.message_id
            await self.call.message.edit_text("Ожидайте второго игрока", reply_markup=await self.keyboard_check())
        if self.castle["start_one"] == -1 and self.castle["start_two"] == -1:
            self.castle["start_one"] = 0
            self.castle["start_two"] = 0
            await castle_place_troops(self.castle)
            que = self.castle["que"]
            move_2 = self.castle["q"][que]
            text = "Бой начался\n"
            await self.castle_edit_message(text, text, move_2)

    async def keyboard_check(self):
        keyboard_c = InlineKeyboardMarkup()
        keyboard_c.row(InlineKeyboardButton("✅ Готов", callback_data=f"castle_check"))
        return keyboard_c

    async def castle_pole_hit(self):
        print("castle_pole_hit")
        try:
            if self.call_data.split("_")[2] == "one" and self.castle["user_one"] == self.user_id:
                text = "Ячейка занята твоими войсками"
                await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
            elif self.call_data.split("_")[2] == "two" and self.castle["user_two"] == self.user_id:
                text = "Ячейка занята твоими войсками"
                await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
            else:
                print("castle_pole_hit_удар_соперника")
                move_all = self.call_data.split("_")[2]
                print(move_all)
                move_q = self.castle["que"]
                print(move_q)
                move_1 = self.castle["q"][move_q]
                print(move_1)
                go_move_1 = move_1.split("_")[1]
                print(go_move_1)
                if go_move_1 == move_all:
                    print("Ожидайте, ходит соперник")
                else:
                    hit = "%s_%s" % (self.call_data.split("_")[1], self.call_data.split("_")[2])
                    if await castle_hit(self.castle, move_1, hit) == False:
                        text = "Вы слишком далеко"
                        await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
                    else:
                        print("castle_pole_hit_2")
                        print(self.castle["q"])
                        que = self.castle["que"]
                        print(f"que {que}")
                        try:
                            move_2 = self.castle["q"][que]
                            print(f"move_2_try {move_2}")
                        except IndexError:
                            try:
                                move_2 = self.castle["q"][que + 1]
                                print(f"move_2_except_try {move_2}")
                            except IndexError:
                                self.castle["que"] = 0
                                print(f"self.castle {self.castle['que']}")
                                move_2 = self.castle["q"][0]
                                print(f"move_2_except_except {move_2}")
                        self.n = int(self.castle["field"].index(move_2))
                        print(f"n {self.n}")
                        print(self.castle["q"])
                        print(self.castle["field"])
                        await self.castle_pole_step()

        except TypeError:
            print("castle_pole_hit_IndexError_3")

    async def castle_pole_step(self):
        print("castle_pole_step")
        try:
            n = int(self.call.data.split("_")[1])
        except ValueError:
            n = self.n
        k = 0
        while k < len(self.castle["field"]):
            if self.castle["field"][k] == 1:
                self.castle["field"][k] = 0
            elif self.castle["field"][k] == 3:
                self.castle["field"][k] = 0
            else:
                pass
            k += 1
        que = self.castle["que"]
        print(f"castle_pole_step {self.castle['q']}")
        print(f"castle_pole_step {self.castle['field']}")
        if self.castle["que"] == len(self.castle["q"]) - 1:
            move_1 = self.castle["q"][que]
            self.castle["que"] = -1
            move_2 = self.castle["q"][self.castle["que"] + 1]
        else:
            move_1 = self.castle["q"][que]
            move_2 = self.castle["q"][que + 1]
        print(f"castle_pole_step_2 {self.castle['q']}")
        print(f"castle_pole_step_2 {self.castle['field']}")
        if await self.check_warrior() == False:
            return
        else:
            text_1, text_2 = "Бой начался", "Бой начался"

            if self.call_data == "step_break":
                pass
            else:
                nn = self.castle["field"].index(move_1)
                self.castle["field"][n] = move_1
                if self.call_data.split("_")[0] != 'hit':
                    self.castle["field"][nn] = 0
            self.castle["goto"] = move_2
            self.castle["que"] += 1
            print(f"castle_pole_step_3 {self.castle['q']}")
            print(f"castle_pole_step_3 {self.castle['field']}")
            await self.castle_edit_message(text_1, text_2, move_2)

    async def castle_pole_break(self):
        print("castle_pole_break")
        que = self.castle["que"]
        move_2 = self.castle["q"][que]
        self.n = int(self.castle["field"].index(move_2))
        await self.castle_pole_step()

    async def check_warrior(self):
        print("check_warrior")
        check = []
        for t in self.castle["q"]:
            check.append(t.split("_")[1])
        if "one" in check:
            pass
        else:
            text_one = "Вы проиграли, вы убили %s юнитов" % self.castle["dead_one"]
            text_two = "Вы победили, вы убили %s юнитов" % self.castle["dead_two"]
            bot.send_message(chat_id=self.castle["user_one"], text=text_one,
                             reply_markup=keyboard.keyboard_main_menu())
            bot.send_message(chat_id=self.castle["user_two"], text=text_two,
                             reply_markup=keyboard.keyboard_main_menu())
            try:
                bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
                bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
            except Exception as n:
                print("Error_castle_escape_field_1_%s" % n)
            self.all_castle.pop(self.key)
            return False
        if "two" in check:
            pass
        else:
            text_two = "Вы проиграли, вы убили %s юнитов" % self.castle["dead_two"]
            text_one = "Вы победили, вы убили %s юнитов" % self.castle["dead_one"]
            bot.send_message(chat_id=self.castle["user_one"], text=text_one,
                             reply_markup=keyboard.keyboard_main_menu())
            bot.send_message(chat_id=self.castle["user_two"], text=text_two,
                             reply_markup=keyboard.keyboard_main_menu())
            try:
                bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
                bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
            except Exception as n:
                print("Error_castle_escape_field_2_%s" % n)
            self.all_castle.pop(self.key)
            return False

    async def castle_escape(self):
        print("castle_escape")
        try:
            if self.user_id == self.castle["user_one"]:
                await self.message.answer(text="Вы сбежали", reply_markup=keyboard.keyboard_main_menu())
                self.all_castle.pop(self.key)
        except AttributeError:
            await self.message.answer("Меню", reply_markup=keyboard.keyboard_main_menu())

    def castle_keyboard_start(self):
        keyboard_one = InlineKeyboardMarkup()
        keyboard_two = InlineKeyboardMarkup()
        keyboard_one.row(InlineKeyboardButton("Подтвердить", callback_data=f"castle_auto_{self.castle['user_one']}"))
        keyboard_one.row(InlineKeyboardButton("Отказаться", callback_data=f"castle_manual_{self.castle['user_one']}"))
        keyboard_two.row(InlineKeyboardButton("Подтвердить", callback_data=f"castle_auto_{self.castle['user_two']}"))
        keyboard_two.row(InlineKeyboardButton("Отказаться", callback_data=f"castle_manual_{self.castle['user_two']}"))
        return keyboard_one, keyboard_two

    async def castle_edit_message(self, text_1, text_2, move_2):
        print("castle_edit_message")
        keyboard_one, keyboard_two = await self.castle_keyboard_castle(move_2, "warrior")
        await bot.edit_message_text(text=text_1, message_id=self.castle["chat_id_one"],
                                    chat_id=self.castle["user_one"], reply_markup=keyboard_one)
        await bot.edit_message_text(text=text_2, message_id=self.castle["chat_id_two"],
                                    chat_id=self.castle["user_two"], reply_markup=keyboard_two)

    async def timer(self, status="null"):
        await asyncio.sleep(30)
        if self.castle["start_one"] == -2:
            print("Вы не подтердили участия")
            # await bot.send_message(text="Второй игрок не подтвердил своё участие\n",
            #                        chat_id=self.castle["user_one"])
            # await bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_two"],
            #                        reply_markup=keyboard.keyboard_main_menu())
            # await self.castle_escape()
        if self.castle["start_two"] == -2:
            print("Второй игрок не подтердил участия")
            # await bot.send_message(text="Второй игрок не подтвердил своё участие\n",
            #                        chat_id=self.castle["user_two"])
            # await bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_one"],
            #                        reply_markup=keyboard.keyboard_main_menu())
            # await self.castle_escape()

    async def castle_keyboard_castle(self, move_2, warrior):
        print("castle_keyboard_castle")
        print(f"castle_keyboard_castle_1 {self.castle['q']}")
        print(f"castle_keyboard_castle_1 {self.castle['field']}")
        await castle_battle(self.castle)
        print(f"castle_keyboard_castle_2 {self.castle['q']}")
        print(f"castle_keyboard_castle_2 {self.castle['field']}")
        keyboard_one = InlineKeyboardMarkup()
        keyboard_two = InlineKeyboardMarkup()
        x, y, n, s = 0, 0, 0, 8
        one = ["user_one", "barracks_one", "shooting_one", "stable_one"]
        two = ["user_two", "barracks_two", "shooting_two", "stable_two", "tower_two"]
        while x < s:
            tab_one = []
            tab_two = []
            y = 0
            while y < s:
                if self.castle["field"][n] == "user_one":
                    tab_one.append(InlineKeyboardButton("🚶‍♂", callback_data="hit_user_one"))
                    tab_two.append(InlineKeyboardButton("🚶‍♂", callback_data="hit_user_one"))

                elif self.castle["field"][n] == "user_two":
                    tab_one.append(InlineKeyboardButton("🚶‍♂", callback_data="hit_user_two"))
                    tab_two.append(InlineKeyboardButton("🚶‍♂", callback_data="hit_user_two"))

                elif self.castle["field"][n] == "barracks_one":
                    tab_one.append(InlineKeyboardButton("⚔", callback_data="hit_barracks_one"))
                    tab_two.append(InlineKeyboardButton("⚔", callback_data="hit_barracks_one"))

                elif self.castle["field"][n] == "barracks_two":
                    tab_one.append(InlineKeyboardButton("⚔", callback_data="hit_barracks_two"))
                    tab_two.append(InlineKeyboardButton("⚔", callback_data="hit_barracks_two"))

                elif self.castle["field"][n] == "shooting_one":
                    tab_one.append(InlineKeyboardButton("🏹", callback_data="hit_shooting_one"))
                    tab_two.append(InlineKeyboardButton("🏹", callback_data="hit_shooting_one"))

                elif self.castle["field"][n] == "shooting_two":
                    tab_one.append(InlineKeyboardButton("🏹", callback_data="hit_shooting_two"))
                    tab_two.append(InlineKeyboardButton("🏹", callback_data="hit_shooting_two"))

                elif self.castle["field"][n] == "stable_one":
                    tab_one.append(InlineKeyboardButton("🐴", callback_data="hit_stable_one"))
                    tab_two.append(InlineKeyboardButton("🐴", callback_data="hit_stable_one"))
                elif self.castle["field"][n] == "stable_two":
                    tab_one.append(InlineKeyboardButton("🐴", callback_data="hit_stable_two"))
                    tab_two.append(InlineKeyboardButton("🐴", callback_data="hit_stable_two"))
                elif self.castle["field"][n] == 3:
                    tab_one.append(InlineKeyboardButton("💥", callback_data="start_null"))
                    tab_two.append(InlineKeyboardButton("💥", callback_data="hit_tower_two"))
                elif self.castle["field"][n] == 1 and move_2 in one:
                    tab_one.append(InlineKeyboardButton("✳", callback_data="step_%s" % n))
                    tab_two.append(InlineKeyboardButton(" ", callback_data="l_%s" % n))
                elif self.castle["field"][n] == 1 and move_2 in two:
                    tab_one.append(InlineKeyboardButton(" ", callback_data="l_%s" % n))
                    tab_two.append(InlineKeyboardButton("✳", callback_data="step_%s" % n))
                elif self.castle["field"][n] == "tower_two":
                    tab_one.append(InlineKeyboardButton("⛩", callback_data="step_null"))
                    tab_two.append(InlineKeyboardButton("⛩", callback_data="l_%s"))


                # elif key["field"][n] == 3 and str(call.message.chat.id) == str(key["user_two"]):
                #     tab_one.append(InlineKeyboardButton("🗡", callback_data="start_null"))
                #     tab_two.append(InlineKeyboardButton(" ", callback_data="start_null"))

                else:
                    tab_one.append(InlineKeyboardButton(" ", callback_data="step_field"))
                    tab_two.append(InlineKeyboardButton(" ", callback_data="step_field"))
                y += 1
                n += 1
            keyboard_one.row(*tab_one)
            keyboard_two.row(*tab_two)
            x += 1

        # text_one, text_two = text_total_war(key, warrior)
        # keyboard_one.row(InlineKeyboardButton(text_one, callback_data="step_null"))
        # keyboard_two.row(InlineKeyboardButton(text_two, callback_data="step_null"))
        if move_2 in one:
            keyboard_one.row(InlineKeyboardButton("Пропустить ход", callback_data="step_break"))
            keyboard_two.row(InlineKeyboardButton("Ход соперника", callback_data="step_null"))
        elif move_2 in two:
            keyboard_two.row(InlineKeyboardButton("Пропустить ход", callback_data="step_break"))
            keyboard_one.row(InlineKeyboardButton("Ход соперника", callback_data="step_null"))
        return keyboard_one, keyboard_two
    #         elif self.call_data == "start_busy":
    #             bot.answer_callback_query(callback_query_id=self.call_id, text="Поле уже занято")
    #             pass
    #         elif self.call_data == "start_null":
    #             bot.answer_callback_query(callback_query_id=self.call_id, text="Поле не активно")
    #             pass
    #         elif self.call_data == "step_break":
    #             que = self.castle["que"]
    #             move_2 = self.castle["q"][que]
    #             n = int(self.castle["field"].index(move_2))
    #             self.castle_step(n)

async def castle_place_troops(key):
    print("castle_place_troops")
    key["field"] = [0 for i in range(0, 64)]
    key["goto"] = key["q"][0]
    i = 0
    while i < len(key["field"]):
        if key["field_one"][i] != 0:
            key["field"][i] = key["field_one"][i]
        elif key["field_two"][i] != 0:
            key["field"][i] = key["field_two"][i]
        i += 1
    key["q"].append("user_one")
    key["q"].append("user_two")
    key["q"].append("tower_two")
    for t in key["q"]:
        if t == "user_one":
            key["field"][0] = t
            # await castle_place_troops_random("t_one", key, t)
        elif t == "user_two":
            key["field"][7] = t
            # await castle_place_troops_random("t_two", key, t)
        elif t == "barracks_one":
            await castle_place_troops_random("t_one", key, t)
        elif t == "barracks_two":
            await castle_place_troops_random("t_two", key, t)
        elif t == "shooting_one":
            await castle_place_troops_random("t_one", key, t)
        elif t == "shooting_two":
            await castle_place_troops_random("t_two", key, t)
        elif t == "stable_one":
            await castle_place_troops_random("t_one", key, t)
        elif t == "stable_two":
            await castle_place_troops_random("t_two", key, t)
        elif t == "tower_two":
            key["field"][63] = t

async def castle_place_troops_random(user, key, t):
    print("castle_place_troops_random")
    r = random.choice(key[user])
    key["field"][r] = t
    key[user].remove(r)

def text_total_war(key, warrior):
    print("text_total_war")
    lvl_war = str(key["lvl_war"])
    user_one = str(key["user_one"])
    user_two = str(key["user_two"])
    text_one = "⚔: %s️🏹: %s 🐴: %s" % \
               (warrior[user_one]["barracks"][lvl_war], warrior[user_one]["shooting"][lvl_war],
                warrior[user_one]["stable"][lvl_war])
    text_two = "⚔: %s️🏹: %s 🐴: %s" % \
               (warrior[user_two]["barracks"][lvl_war], warrior[user_two]["shooting"][lvl_war],
                warrior[user_two]["stable"][lvl_war])
    return text_one, text_two

async def castle_battle(key):
    print("castle_battle")
    # for ss in key["field"]:
    #     if ss == key["goto"]:
    if key["goto"] == "user_one":
        await castle_calculation(key, "user_one")
    elif key["goto"] == "user_two":
        await castle_calculation(key, "user_two")
    elif key["goto"] == "barracks_one":
        await castle_calculation(key, "barracks_one")
    elif key["goto"] == "barracks_two":
        await castle_calculation(key, "barracks_two")
    elif key["goto"] == "shooting_one":
        await castle_calculation(key, "shooting_one")
    elif key["goto"] == "shooting_two":
        await castle_calculation(key, "shooting_two")
    elif key["goto"] == "stable_one":
        await castle_calculation(key, "stable_one")
    elif key["goto"] == "stable_two":
        await castle_calculation(key, "stable_two")
    elif key["goto"] == "tower_two":
        await castle_calculation(key, "tower_two")
    print(key['q'])
    print(key['field'])

async def castle_calculation(key, data):
    print("castle_calculation")
    nn = key["field"].index(data)
    move = data.split("_")[0]
    user = data.split("_")[1]
    if move == "user":
        pole = [-8, -1, 0, 1, 8]
        await castle_cal_pole(key, pole, nn, 1)
    if move == "barracks":
        pole = [-9, -7, -8, -1, 0, 1, 8, 7, 9]
        await castle_cal_pole(key, pole, nn, 1)
    if move == "stable":
        pole = [-16, -2, -8, -1, 0, 1, 8, 2, 16]
        await castle_cal_pole(key, pole, nn, 1)
    if move == "shooting":
        pole = [-8, -1, 0, 1, 8]
        await castle_cal_pole(key, pole, nn, 1)
    if move == "tower":
        pole = await castle_tower_field()
        await castle_cal_pole(key, pole, nn, 3)

async def castle_tower_field():
    print("castle_tower_field")
    r = random.randint(0, 7)
    pole = [[-63, -62, -61, -60, -59, -58, -57, -56],
            [-55, -54, -53, -52, -51, -50, -49, -48],
            [-47, -46, -45, -44, -43, -42, -41, -40],
            [-39, -38, -37, -36, -35, -34, 33, -32],
            [-31, -30, -29, -28, -27, -26, -25, -24],
            [-23, -22, -21, -20, -19, -18, -17, -16],
            [-15, -14, -13, -12, -11, -10, -9, -8],
            [-7, -6, -5, -4, -3, -2, -1, 0]]
    return pole[r]

async def castle_cal_pole(key, pole, nn, kof):
    print("castle_cal_pole")
    if kof == 3:
        cell_null = []
        cell_old = []
    else:
        cell_null = [0, 1, 8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57]
        cell_old = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55, 62, 63]
    for g in pole:
        if nn in cell_null:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0 and nn + g not in cell_old:
                    key["field"][nn + g] = kof

        if nn in cell_old:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0 and nn + g not in cell_null:
                    key["field"][nn + g] = kof

        if nn not in cell_null and nn not in cell_old:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0:
                    key["field"][nn + g] = kof

    #
    #     def castle_edit_message(self, text_1, text_2, move_2):
    #         keyboard_one, keyboard_two = battle_castle.castle_keyboard_castle(self.castle, move_2, warrior)
    #         bot.edit_message_text(text=text_1, message_id=self.castle["chat_id_one"],
    #                               chat_id=self.castle["user_one"], reply_markup=keyboard_one)
    #         bot.edit_message_text(text=text_2, message_id=self.castle["chat_id_two"],
    #                               chat_id=self.castle["user_two"], reply_markup=keyboard_two)
    #
    #     def timer(self, status="null"):
    #         global t
    #         if status == "start":
    #             print("Start_timer_1")
    #             t = threading.Timer(30, self.timer)
    #             t.start()
    #             print("Start_timer_2")
    #         elif status == "stop":
    #             print("Stop_timer_1")
    #             t.cancel()
    #             print("Stop_timer_2")
    #         else:
    #             print("ТАймер не остановлен")
    #             if self.castle["start_one"] == -1:
    #                 bot.send_message(text="Второй игрок не подтвердил своё участие\n", chat_id=self.castle["user_one"])
    #                 bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_two"],
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 self.castle_escape()
    #             elif self.castle["start_two"] == -1:
    #                 bot.send_message(text="Второй игрок не подтвердил своё участие\n", chat_id=self.castle["user_two"])
    #                 bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_one"],
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 self.castle_escape()
    #



    #     def castle_escape_field(self):
    #         try:
    #             if self.message_chat_id == self.castle["user_one"]:
    #                 print("Нападал")
    #                 bot.send_message(chat_id=self.castle["user_one"], text="Вы сбежали и програли",
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 bot.send_message(chat_id=self.castle["user_two"], text="Соперник сбежал, вы победили",
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 try:
    #                     bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
    #                 except Exception as n:
    #                     print("Error_castle_escape_field_1_%s" % n)
    #                 print(self.all_castle)
    #                 print(self.key)
    #                 self.all_castle.pop(self.key)
    #                 print(self.all_castle)
    #
    #             elif self.message_chat_id == self.castle["user_two"]:
    #                 print("Защищался")
    #                 bot.send_message(chat_id=self.castle["user_two"], text="Вы сбежали и програли",
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 bot.send_message(chat_id=self.castle["user_one"], text="Соперник сбежал, вы победили",
    #                                  reply_markup=keyboard.keyboard_main_menu())
    #                 try:
    #                     bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
    #                 except Exception as n:
    #                     print("Error_castle_escape_field_2_%s" % n)
    #                 self.all_castle.pop(self.castle)
    #         except TypeError:
    #             print("castle_escape_field_TypeError")
    #             bot.send_message(chat_id=self.message_chat_id, text="Главное меню",
    #                              reply_markup=keyboard.keyboard_main_menu())
    #

    #
    # async def save_castle():
    #     global castle
    #     with open(PATH + "tmp/castle.json", 'w', encoding="utf-16") as f:
    #         json.dump(castle, f)
    #     with open(PATH + "tmp/castle.json", 'rb') as f:
    #         castle = json.load(f)
    #
    #
    # def open_castle():
    #     global castle
    #     with open(PATH + "tmp/" + 'castle.json', 'rb') as f:
    #         castle = json.load(f)
    #
    #
    # open_castle()

    # def castle_start_queue(one, two, lvl_war, warrior):
    #     print("castle_start_queue_1")
    #     stat_one = (sorted(warrior[str(one)].items(), key=lambda k: k[1][str(lvl_war)]))
    #     stat_two = (sorted(warrior[str(two)].items(), key=lambda k: k[1][str(lvl_war)]))
    #     queue = {"q": [], "q_one": [], "q_two": []}
    #     for key, value in stat_one:
    #         if value[str(lvl_war)] == 0:
    #             pass
    #         else:
    #             queue["q_one"].append(key)
    #
    #     for key, value in stat_two:
    #         if value[str(lvl_war)] == 0:
    #             pass
    #         else:
    #             queue["q_two"].append(key)
    #     #    print(queue["q_one"])
    #     if queue["q_one"] == []:
    #         print("У вас нет воинов %s уровня" % lvl_war)
    #         return "У вас нет воинов %s уровня" % lvl_war
    #     if queue["q_two"] == []:
    #         print("У соперника нет воинов %s уровня" % lvl_war)
    #         return "У соперника нет воинов %s уровня" % lvl_war
    #
    #     i = 0
    #     while i < 3:
    #         try:
    #             queue["q"].append("%s_one" % queue["q_one"][i])
    #         except:
    #             pass
    #
    #         try:
    #             queue["q"].append("%s_two" % queue["q_two"][i])
    #         except:
    #             pass
    #         i += 1
    #     queue.pop("q_one")
    #     queue.pop("q_two")
    #     castle = {"user_one": one, "user_two": two, "lvl_war": str(lvl_war), "start_one": 0, "start_two": 0,
    #               "chat_id_one": 0, "chat_id_two": 0, "dead_one": 0, "dead_two": 0,
    #               "goto": " ", "que": 0, "q": queue["q"], "field": [], "t_one": [0, 16, 32, 48], "t_two": [63, 47, 31, 15]}
    #     castle = {"user_one": one, "user_two": two, "lvl_war": str(lvl_war), "start_one": 0, "start_two": 0,
    #               "chat_id_one": 0, "chat_id_two": 0, "dead_one": 0, "dead_two": 0,
    #               "goto": " ", "que": 0, "q": queue["q"], "field": [], "t_one": [19, 35], "t_two": [20, 36]}
    #     print(castle)
    #     return castle





    # elif self.call_data == "start_busy":
    #     await bot.answer_callback_query(callback_query_id=self.call_id, text="Поле уже занято")
    # elif self.call_data == "start_null":
    #     await bot.answer_callback_query(callback_query_id=self.call_id, text="Поле не активно")






#
#
# # def text_message(key, move_1):
# #     print("text_message")
# #     text_1, text_2 = "null", "null"
# #     if move_1 == "user_one":
# #         text_2 = "Ходите героем"
# #         text_1 = "Ожидайте хода соперника"
# #     elif move_1 == "barracks_one":
# #         text_2 = "Ходите воинами"
# #         text_1 = "Ожидайте хода соперника"
# #     elif move_1 == "shooting_one":
# #         text_2 = "Ходите лучниками"
# #         text_1 = "Ожидайте хода соперника"
# #     elif move_1 == "stable_one":
# #         text_2 = "Ходите всадниками"
# #         text_1 = "Ожидайте хода соперника"
# #     elif move_1 == "user_two":
# #         text_1 = "Ходите воинами"
# #         text_2 = "Ожидайте хода соперника"
# #     elif move_1 == "barracks_two":
# #         text_1 = "Ходите лучниками"
# #         text_2 = "Ожидайте хода соперника"
# #     elif move_1 == "shooting_two":
# #         text_1 = "Ходите всадниками"
# #         text_2 = "Ожидайте хода соперника"
# #     elif move_1 == "stable_two":
# #         text_1 = "Ходите героем"
# #         text_2 = "Ожидайте хода соперника"
# #     return text_1, text_2
#
#
async def castle_hit(key, move_1, hit):
    print("castle_hit")
    move = move_1.split("_")[0]
    hit_one = key["field"].index(move_1)
    hit_two = key["field"].index(hit)
    hit_old = hit_one - hit_two
    pole = []
    print(move)
    print(f"one {hit_one}")
    print(f"two {hit_two}")
    print(hit_old)
    st_one = [0, 8, 16, 24, 32, 40, 48, 56,7, 15, 23, 31, 39, 47, 55, 63]
    # st_two = [7, 15, 23, 31, 39, 47, 55, 63]
    if hit_two in st_one or hit_one in st_one:
        print("false")
        return False

    if move == "user":
        pole = [-8, -1, 1, 8]
        # cal_pole_one(key, pole, nn, 1)
    if move == "barracks":
        pole = [-9, -7, -8, -1, 1, 8, 7, 9]
        # cal_pole_one(key, pole, nn, 1)
    if move == "stable":
        pole = [-16, -2, -8, -1, 1, 8, 2, 16]
        # cal_pole_one(key, pole, nn, 1)
    if move == "shooting":
        pole = [-8, -1, 1, 8]
        # cal_pole_one(key, pole, nn, 1)
    if hit_old in pole:
        war_one = move_1.split("_")[0]
        war_two = hit.split("_")[0]
        # Воины - Лучники
        if war_one == "barracks" and war_two == "shooting":
            koef = 1.25
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # Воины - Всадники
        elif war_one == "barracks" and war_two == "stable":
            koef = 0.75
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # Лучники - Воины
        elif war_one == "shooting" and war_two == "barracks":
            koef = 0.75
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # Лучники - Всадники
        elif war_one == "shooting" and war_two == "stable":
            koef = 1.25
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # Всадники - Воины
        elif war_one == "stable" and war_two == "barracks":
            koef = 1.25
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # Всадники - Лучники
        elif war_one == "stable" and war_two == "shooting":
            koef = 0.75
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        else:
            koef = 1
            n = await calculation_hit(key, koef, move_1, hit)
            return n
        # key["q"].remove(hit)
        # # key["field"][hit_one] = 0
        # # key["field"][hit_two] = move_1
        # return hit_two
    else:
        return False


async def calculation_hit(key, koef, move_1, hit):
    print("calculation_hit")
    hit_one = key["field"].index(move_1)
    print(f"hit_one {hit_one}")
    hit_two = key["field"].index(hit)
    print(f"hit_two {hit_two}")
    war_one = move_1.split("_")[0]
    print(f"war_one {war_one}")
    war_two = hit.split("_")[0]
    print(f"war_two {war_two}")
    lvl_war = str(key["lvl_war"])
    user_one = str(key["user_one"])
    user_two = str(key["user_two"])
    req_one = f"""SELECT hit, defence, health, {war_one} FROM training INNER JOIN warrior 
ON training.lvl = warrior.lvl 
WHERE name = '{war_one}' and training.lvl = {lvl_war} and user_id = {user_one}"""
    req_two = f"""SELECT hit, defence, health, {war_two} FROM training INNER JOIN warrior 
ON training.lvl = warrior.lvl 
WHERE name = '{war_two}' and training.lvl = {lvl_war} and user_id = {user_two}"""
    attack_one, defence_one, health_one, num_one = await sql_selectone(req_one)
    attack_two, defence_two, health_two, num_two = await sql_selectone(req_two)

    # num_one = int(warrior[user_one][war_one][lvl_war])
    # num_two = int(warrior[user_two][war_two][lvl_war])
    # attack_one = training[war_one][int(lvl_war)]["attack"]
    # attack_two = training[war_two][int(lvl_war)]["attack"]
    # defence_one = training[war_one][int(lvl_war)]["defence"]
    # defence_two = training[war_two][int(lvl_war)]["defence"]
    # health_one = training[war_one][int(lvl_war)]["health"]
    # health_two = training[war_two][int(lvl_war)]["health"]
    stat_one = num_one * attack_one * health_one * koef
    stat_two = num_two * defence_two * health_two
    total = stat_one - stat_two
    print(f"stat_one {stat_one}")
    print(f"stat_two {stat_two}")
    print(f"total {total}")
    print(f"Очередь до боя {key['q']}")
    print(f"поле до боя {key['field']}")
    if total == 0:
        print("total 0")

        key["field"][hit_two] = 0
        key["field"][hit_one] = 0
        key["q"].remove(move_1)
        key["q"].remove(hit)
        print(f"Очередь после боя {key['q']}")
        print(f"поле после боя {key['field']}")
            # warrior[user_one][war_one][lvl_war] = 0
            # warrior[user_two][war_two][lvl_war] = 0
    elif total < 0:
        print("total < 0")
        key["q"].remove(move_1)
        key["field"][hit_one] = 0
        print(f"Очередь после боя {key['q']}")
        print(f"поле после боя {key['field']}")
            # warrior[user_one][war_one][lvl_war] = 0
            # warrior[user_two][war_two][lvl_war] = int(total / defence_two / health_two) * -1
            # move_2 = key["q"][key["que"]]
            # n = int(key["field"].index(move_2))
            # return n

            # # key["field"][hit_one] = move_1
        # key["dead_one"] += num_two + int(total / defence_two / health_two)
        # key["dead_two"] += num_one

    else:
        print("Убил всех")
        print(total / attack_one / health_one)
        key["q"].remove(hit)
        key["field"][hit_two] = 0
        print(f"Очередь после боя {key['q']}")
        print(f"поле после боя {key['field']}")
            # warrior[user_two][war_two][lvl_war] = 0
            # warrior[user_one][war_one][lvl_war] -= int(total / attack_one / health_one)

            # key["field"][hit_one] = 0

        # key["dead_one"] += num_one
        # key["dead_two"] += int(total / attack_one / health_one)
            # return hit_two





#     #     # pole = [-32, -24, -16, -8, -23, -15, -7, -14, -6, -5, 1, 2, 3, 4, 8, 9, 10, 11, 16, 17, 18, 24, 25, 32]
#     #     # cal_pole_one(key, pole, nn, 3)
#     # print(hit_one)
#     # print(hit_two)
#     # # print(pole)
#     # data = hit_one - hit_two
#     # if data in pole:
#     #     print("Удар от %s по %s" % (move_1, hit))
#     #     print(key["q"])
#     #     # key["q"].remove(hit)
#     #     # print(key["q"])
#     #
#     # else:
#     #     print("Промах")
#
#
# #     # if data == "tower":
# #     #     pole = [-8, -1, 1, 8]
# #     #     cal_pole_one(key, pole, nn, 3)
# # #
#
# class Castle():
#     def __init__(self, message, call=""):
#         self.st_one = [0, 8, 16, 24, 32, 40, 48, 56]
#         self.st_two = [7, 15, 23, 31, 39, 47, 55, 63]
#         try:
#             self.message = message
#             self.text = message.text
#             self.message_chat_id = message.chat.id
#         except:
#             print("castle_error_1")
#         try:
#             self.call = call
#             self.message = call.message
#             self.call_data = call.data
#             self.call_id = call.id
#             self.call_message_id = call.message.message_id
#             self.message_chat_id = call.message.chat.id
#         except:
#             print("castle_error_2")
#         try:
#             self.key = self.search_castle()
#             self.castle = castle[self.key]
#             self.all_castle = castle
#
#         except:
#             print("castle_error_3")
#
#     def search_castle(self):
#         for key, value in castle.items():
#             if str(self.message_chat_id) == key.split("_")[0]:
#                 return key
#             elif str(self.message_chat_id) == key.split("_")[1]:
#                 return key
#
#     async def castle_pole(self, pos=""):
#         print("pos %s" % pos)
#         if self.text == texting.button_castle_attack:
#             print(texting.button_castle_attack)
#             self.castle["field_one"] = [0 for i in range(0, 64)]
#             self.castle["field_two"] = [0 for i in range(0, 64)]
#             text_one, text_two = "Вы атаковали замок\n", "Ваш замок атаковали\n"
#             keyboard_one, keyboard_two = castle_keyboard_start(self.castle)
#             await bot.send_message(chat_id=self.castle["user_one"], text=text_one,
#                              reply_markup=keyboard.keyboard_castle_escape_field())
#             await bot.send_message(chat_id=self.castle["user_two"], text=text_two,
#                              reply_markup=keyboard.keyboard_castle_escape_field())
#             await bot.send_message(text="----->", chat_id=self.castle["user_one"], reply_markup=keyboard_one)
#             await bot.send_message(text="<-----", chat_id=self.castle["user_two"], reply_markup=keyboard_two)
#             await self.timer("start")
#         elif self.call_data == "start_busy":
#             await bot.answer_callback_query(callback_query_id=self.call_id, text="Поле уже занято")
#         elif self.call_data == "start_null":
#             await bot.answer_callback_query(callback_query_id=self.call_id, text="Поле не активно")
#         elif self.call_data == "step_break":
#             que = self.castle["que"]
#             move_2 = self.castle["q"][que]
#             n = int(self.castle["field"].index(move_2))
#             await self.castle_step(n)
#         elif self.call_data.split("_")[0] == "step":
#             print("ok")
#             n = int(self.call_data.split("_")[1])
#             await self.castle_step(n)
#         elif self.call_data.split("_")[0] == "castle":
#             print("castle")
#             if self.message_chat_id == self.castle["user_one"]:
#                 self.castle["start_one"] = -1
#                 self.castle["chat_id_one"] = self.call_message_id
#             elif self.message_chat_id == self.castle["user_two"]:
#                 self.castle["start_two"] = -1
#                 self.castle["chat_id_two"] = self.call_message_id
#             if self.castle["start_one"] == -1 and self.castle["start_two"] == -1:
#                 await self.timer("stop")
#                 self.castle["start_one"] = 0
#                 self.castle["start_two"] = 0
#                 print("castle_1")
#                 await castle_place_troops(self.castle)
#                 print("castle_2")
#                 que = self.castle["que"]
#                 move_2 = self.castle["q"][que]
#                 text = "Бой начался\n"
#                 await self.castle_edit_message(text, text, move_2)
#         elif self.call_data.split("_")[0] == "hit":
#             try:
#                 if self.call_data.split("_")[2] == "one" and self.castle["user_one"] == self.message_chat_id:
#                     print("Ячейка занята твоими войсками")
#                     text = "Ячейка занята твоими войсками"
#                     await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
#                 elif self.call_data.split("_")[2] == "two" and self.castle["user_two"] == self.message_chat_id:
#                     print("Ячейка занята твоими войсками")
#                     text = "Ячейка занята твоими войсками"
#                     await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
#                 else:
#                     move_all = self.call_data.split("_")[2]
#                     move_q = self.castle["que"]
#                     move_1 = self.castle["q"][move_q]
#                     go_move_1 = move_1.split("_")[1]
#                     if go_move_1 == move_all:
#                         print("Ожидайте, ходит соперник")
#                     else:
#                         hit = "%s_%s" % (self.call_data.split("_")[1], self.call_data.split("_")[2])
#                         print("hit_1")
#
#                         # self.castle_step(n)
#                         if castle_hit(self.castle, move_1, hit, warrior) == False:
#                             text = "Вы слишком далеко"
#                             await bot.answer_callback_query(callback_query_id=self.call_id, text=text)
#                         else:
#                             que = self.castle["que"]
#                             print("Следующий ход %s" % que)
#                             try:
#                                 move_2 = self.castle["q"][que]
#                             except IndexError:
#                                 print("castle_pole_hit_IndexError_1")
#                                 try:
#                                     move_2 = self.castle["q"][que + 1]
#                                 except IndexError:
#                                     print("castle_pole_hit_IndexError_2")
#                                     self.castle["que"] = 0
#                                     move_2 = self.castle["q"][0]
#                             print("Следующий ход %s" % move_2)
#                             n = int(self.castle["field"].index(move_2))
#                             # bot.answer_callback_query(callback_query_id=self.call_id, text=text)
#                             print("hit_2")
#                             print(n)
#                             await self.castle_step(n)
#             except TypeError:
#                 print("castle_pole_hit_IndexError_3")
#
#     async def castle_step(self, n):
#         k = 0
#         while k < len(self.castle["field"]):
#             if self.castle["field"][k] == 1:
#                 self.castle["field"][k] = 0
#             elif self.castle["field"][k] == 3:
#                 self.castle["field"][k] = 0
#             else:
#                 pass
#             k += 1
#         que = self.castle["que"]
#         if self.castle["que"] == len(self.castle["q"]) - 1:
#             move_1 = self.castle["q"][que]
#             self.castle["que"] = -1
#             move_2 = self.castle["q"][self.castle["que"] + 1]
#         else:
#             move_1 = self.castle["q"][que]
#             move_2 = self.castle["q"][que + 1]
#         print(self.castle["field"])
#         print("index_old_1 %s" % move_1)
#         print("index_old_2 %s" % move_2)
#         # if self.castle["goto"] == self.castle["q"][self.castle["que"]]:
#         # print("err_step_1")
#         if self.check_warrior() == False:
#             return
#         else:
#             # text_1, text_2 = battle_castle.text_message(self.castle, move_1)
#             print("err_step_1")
#             text_1, text_2 = "Бой начался", "Бой начался"
#             nn = self.castle["field"].index(move_1)
#             print("Удаляем %s, ячейка %s" % (move_1, nn))
#             # print("err_step_2")
#             print(self.castle["field"])
#             # print(self.call_message_id)
#             # if self.call_message_id == "step_break":
#             #     pass
#             # else:
#             print(nn)
#             print(n)
#             print(move_1)
#             print("err_step_2")
#             self.castle["field"][n] = move_1
#             self.castle["field"][nn] = 0
#
#             print("err_step_2-5")
#             self.castle["goto"] = move_2
#             print("err_step_3")
#             self.castle["que"] += 1
#             await self.castle_edit_message(text_1, text_2, move_2)
#
#     async def check_warrior(self):
#         check = []
#         for t in self.castle["q"]:
#             check.append(t.split("_")[1])
#         if "one" in check:
#             print("Войска есть")
#             pass
#         else:
#             print("Войск нет. Проиграл первый")
#             print("Убил первый %s" % self.castle["dead_one"])
#             print("Убил второй %s" % self.castle["dead_two"])
#             text_one = "Вы проиграли, вы убили %s юнитов" % self.castle["dead_one"]
#             text_two = "Вы победили, вы убили %s юнитов" % self.castle["dead_two"]
#             await bot.send_message(chat_id=self.castle["user_one"], text=text_one,
#                              reply_markup=keyboard.keyboard_main_menu())
#             await bot.send_message(chat_id=self.castle["user_two"], text=text_two,
#                              reply_markup=keyboard.keyboard_main_menu())
#             try:
#                 bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
#                 bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
#             except Exception as n:
#                 print("Error_castle_escape_field_1_%s" % n)
#             self.all_castle.pop(self.key)
#             return False
#         if "two" in check:
#             print("Войска есть")
#             pass
#         else:
#             print("Войск нет. Проиграл второй")
#             print("Убил первый %s" % self.castle["dead_one"])
#             print("Убил второй %s" % self.castle["dead_two"])
#             text_two = "Вы проиграли, вы убили %s юнитов" % self.castle["dead_two"]
#             text_one = "Вы победили, вы убили %s юнитов" % self.castle["dead_one"]
#             await bot.send_message(chat_id=self.castle["user_one"], text=text_one,
#                              reply_markup=keyboard.keyboard_main_menu())
#             await bot.send_message(chat_id=self.castle["user_two"], text=text_two,
#                              reply_markup=keyboard.keyboard_main_menu())
#             try:
#                 await bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
#                 await bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
#             except Exception as n:
#                 print("Error_castle_escape_field_2_%s" % n)
#             print(self.all_castle)
#             self.all_castle.pop(self.key)
#             return False
#

#
#     async def timer(self, status="null"):
#         global t
#         if status == "start":
#             print("Start_timer_1")
#             t = threading.Timer(30, self.timer)
#             t.start()
#             print("Start_timer_2")
#         elif status == "stop":
#             print("Stop_timer_1")
#             t.cancel()
#             print("Stop_timer_2")
#         else:
#             print("ТАймер не остановлен")
#             if self.castle["start_one"] == -1:
#                 await bot.send_message(text="Второй игрок не подтвердил своё участие\n", chat_id=self.castle["user_one"])
#                 await bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_two"],
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 self.castle_escape()
#             elif self.castle["start_two"] == -1:
#                 await bot.send_message(text="Второй игрок не подтвердил своё участие\n", chat_id=self.castle["user_two"])
#                 await bot.send_message(text="Бой закончен\n", chat_id=self.castle["user_one"],
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 self.castle_escape()
#
#     # async def castle_escape(self):
#     #     req = f"SELECT id_one, id_two FROM castle WHERE id_one ={self.message_chat_id}"
#     #     print(req)
#     #     row = await sql_selectone(req)
#     #     if row[0] == self.message_chat_id:
#     #         await bot.send_message(chat_id=self.message_chat_id, text="Вы сбежали", reply_markup=keyboard.keyboardmap())
#     #         await bot.send_message(chat_id=row[1], text="Соперник сбежал", reply_markup=keyboard.keyboardmap())
#     #         await sql_insert(f"DELETE FROM castle WHERE id_one = {self.message_chat_id}")
#
#         #     print("Delete_castle_1")
#         #     castle.pop(self.key)
#         #     print("Delete_castle_2")
#
#     async def castle_escape_field(self):
#         try:
#             if self.message_chat_id == self.castle["user_one"]:
#                 print("Нападал")
#                 await bot.send_message(chat_id=self.castle["user_one"], text="Вы сбежали и програли",
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 await bot.send_message(chat_id=self.castle["user_two"], text="Соперник сбежал, вы победили",
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 try:
#                     bot.delete_message(chat_id=self.castle["user_one"], message_id=self.castle["chat_id_one"])
#                 except Exception as n:
#                     print("Error_castle_escape_field_1_%s" % n)
#                 print(self.all_castle)
#                 print(self.key)
#                 self.all_castle.pop(self.key)
#                 print(self.all_castle)
#
#             elif self.message_chat_id == self.castle["user_two"]:
#                 print("Защищался")
#                 await bot.send_message(chat_id=self.castle["user_two"], text="Вы сбежали и програли",
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 await bot.send_message(chat_id=self.castle["user_one"], text="Соперник сбежал, вы победили",
#                                  reply_markup=keyboard.keyboard_main_menu())
#                 try:
#                     bot.delete_message(chat_id=self.castle["user_two"], message_id=self.castle["chat_id_two"])
#                 except Exception as n:
#                     print("Error_castle_escape_field_2_%s" % n)
#                 self.all_castle.pop(self.castle)
#         except TypeError:
#             print("castle_escape_field_TypeError")
#             await bot.send_message(chat_id=self.message_chat_id, text="Главное меню",
#                              reply_markup=keyboard.keyboard_main_menu())
