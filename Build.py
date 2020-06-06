from texting import button_building, text_building_update, button_update, button_market,text_building_resource,text_building_goto,button_back,text_building_up
import sql
from aiogram import types
from load_all import dp, bot, benchmark
from Users import info_heroes


async def building(message):
    if message.text == button_building:
        await message.answer(text=text_building_update % (await info_heroes(message, key="build")), reply_markup=await keyboard_building(message))
    else:
        try:
            await message.edit_text(
                text=text_building_update % (await info_heroes(message, key="build")), reply_markup=await keyboard_building(message))
        except Exception as n:
            print(n)


async def build(call, message, text=""):
    keyboard = types.InlineKeyboardMarkup()
    try:
        print(call.isdigit())
        data = call.split("_")[1]
    except AttributeError:
        data = call.data.split("_")[1]

    try:
        if data == "back":
            await building(message)
            pass
        elif data == "update":
            # call_data = self.call_data.split("_")[2]
            if call == str:
                dat = call.split("_")[2]
            else:
                dat = call.data.split("_")[2]

            row_one = """SELECT wood,stone,iron,food 
                FROM heroes INNER JOIN building 
                ON heroes.%s + 1 = building.lvl 
                WHERE user_id = %s AND data_old = '%s'""" % (dat, message.chat.id, dat)
            row_two = """SELECT wood, stone,iron, food 
                FROM resource 
                WHERE user_id = %s""" % message.chat.id
            # print(row_one)
            # print(row_two)
            row_one = await sql.sql_selectone(row_one)
            row_two = await sql.sql_selectone(row_two)
            if row_two[0] > row_one[0] and row_two[1] > row_one[1] and row_two[2] > row_one[2] \
                    and row_two[3] > row_one[3]:
                row = "SELECT castle,storage, farm,barracks, shooting, stable, wall FROM heroes WHERE user_id = %s"
                row = await sql.sql_selectone(row % message.chat.id)
                if row[0] > row[1]:
                    if dat == "storage":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень 🏚склада")
                        except Exception as n:
                            print(n)
                        print("Увеличить склад")
                        data = "build_storage"
                        await build(data, message)
                elif row[1] > row[2]:
                    if dat == "farm":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень фермы")
                        except Exception as n:
                            print(n)
                        data = "build_farm"
                        await build(data, message)
                elif row[2] > row[3]:
                    if dat == "barracks":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень казармы")
                        except Exception as n:
                            print(n)
                        data = "build_barracks"
                        await build(data, message)
                elif row[3] > row[4]:
                    if dat == "shooting":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень стрельбы")
                        except Exception as n:
                            print(n)
                        data = "build_shooting"
                        await build(data, message)
                elif row[4] > row[5]:
                    if dat == "stable":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень конюшни")
                        except Exception as n:
                            print(n)
                        data = "build_stable"
                        await build(data, message)
                elif row[5] > row[6]:
                    if dat == "wall":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень 🧱 стены")
                        except Exception as n:
                            print(n)
                        data = "build_wall"
                        await build(data, message)
                elif row[6] == row[0]:
                    if dat == "castle":
                        await update(message, dat)
                    else:
                        try:
                            await bot.answer_callback_query(callback_query_id=call.id, text="Увеличьте уровень 🏤 замка")
                        except Exception as n:
                            print(n)
                        data = "build_castle"
                        await build(data, message)
            else:
                await bot.answer_callback_query(callback_query_id=call.id, text="Не хватает ресуров")
        # elif call.data == "market":
        #     print(111)
        #     if call.data.split("_")[2] == "buy" or call.data.split("_")[2] == "sell":
        #         print(222)
        #         try:
        #             if call.data.split("_")[4] == "1000" or call.data.split("_")[4] == "10000":
        #                 self.buysell()
        #         except:
        #             bot.edit_message_text(text=self.market_text(), chat_id=self.message_chat_id,
        #                                   message_id=self.call_message_id,
        #                                   reply_markup=self.keyboard_market_buysell())
        #     else:
        #
        #         bot.edit_message_text(text=self.market_text(), chat_id=self.message_chat_id,
        #                               message_id=self.call_message_id,
        #                               reply_markup=self.keyboard_market())
        else:
            print(data)
            try:
                data = data.split("_")[1]
            except Exception as n:
                print(n)
            request_one = """
            SELECT name, lvl, wood,stone,iron,food 
            FROM heroes INNER JOIN building 
            ON heroes.%s + 1 = building.lvl 
            WHERE user_id = %s AND data_old = '%s'"""
            request_two = """SELECT wood,stone,iron,food from resource Where user_id = %s"""
            request_one = await sql.sql_selectone(request_one % (data, message.chat.id, data))
            request_two = await sql.sql_selectone(request_two % message.chat.id)
            name = request_one[0]
            new_lvl = request_one[1]
            if request_two[0] < request_one[2]:
                text_wood = "%s ⛔" % request_one[2]
            else:
                text_wood = "%s ✅" % request_one[2]
            if request_two[1] < request_one[3]:
                text_stone = "%s ⛔" % request_one[3]
            else:
                text_stone = "%s ✅" % request_one[3]
            if request_two[2] < request_one[4]:
                text_iron = "%s ⛔" % request_one[4]
            else:
                text_iron = "%s ✅" % request_one[4]
            if request_two[3] < request_one[5]:
                text_food = "%s ⛔" % request_one[5]
            else:
                text_food = "%s ✅" % request_one[5]
            text += text_building_resource % (
            name, new_lvl - 1, name, new_lvl, text_stone, text_wood, text_iron, text_food)
            keyboard.row(types.InlineKeyboardButton(text=button_update,
                                                            callback_data="build_update_" + data))

            if data == "storage":
                pass
                # request = await sql.sql_selectone("SELECT capacity FROM building LEFT JOIN building_storage " \
                # "ON building.storage = building_storage.lvl WHERE user_id = %s" % self.message_chat_id)
                # text += "\nВместимость ресурсов: %s" % request[0]
            # elif call_data == "farm":
            #     text += "\nПроизводство ресурсов: " + str(buildings[call_data][lvl]["production"]) + " шт\с"
            if data == "barracks":
                keyboard.row(
                    types.InlineKeyboardButton(text=text_building_goto, callback_data="entry_barracks"))
            elif data == "shooting":
                keyboard.row(
                    types.InlineKeyboardButton(text=text_building_goto, callback_data="entry_shooting"))
            elif data == "stable":
                keyboard.row(
                    types.InlineKeyboardButton(text=text_building_goto, callback_data="entry_stable"))
            keyboard.row(types.InlineKeyboardButton(text=button_back, callback_data="build_back"))
            try:
                await message.edit_text(text=text, reply_markup=keyboard)
            except Exception as n:
                print("123 %s" %n)
                pass
    except Exception as n:
        print("123456 %s" % n)
        pass


async def update(message, dat):
    # dat = self.call_data.split("_")[2]
    req = "Update heroes SET %s = %s + 1 WHERE user_id = %s"
    await sql.sql_insert(req % (dat, dat, message.chat.id))
    req = "SELECT wood,stone,iron, food " \
          "FROM heroes INNER JOIN building " \
          "ON heroes.%s = building.lvl " \
          "WHERE user_id = %s AND data_old = '%s'"
    request = await sql.sql_selectone(req % (dat, message.chat.id, dat))
    req = "Update resource " \
          "SET wood = wood - %s, stone = stone - %s, iron = iron -%s, food = food - %s " \
          "WHERE user_id = %s"
    await sql.sql_insert(req% (request[0], request[1], request[2], request[3], message.chat.id))
    text = text_building_up
    data = "build_%s" % dat
    await build(data, message, text)


async def keyboard_building(message):
    keyboard_build = types.InlineKeyboardMarkup()
    i = 17
    tab = []
    request = "SELECT * FROM heroes WHERE user_id = %s" % message.chat.id
    r = await sql.sql_selectone(request)
    r_r = await sql.sql_select("pragma table_info(heroes)")
    temp = 16
    while i < 24:
        s = await sql.sql_selectone("select * from building where data_old = '%s' and lvl = 1" % r_r[i][1])
        tab.append(
            types.InlineKeyboardButton(text="%s %s" % (s[0], r[i]), callback_data="build_%s" % r_r[i][1]))
        if i == temp + 1 or i == temp + 4 or i == temp + 7:
            keyboard_build.row(*tab)
            tab = []
        i += 1
    keyboard_build.row(*tab)
    keyboard_build.row(types.InlineKeyboardButton(text=button_market, callback_data="build_market_null"))
    return keyboard_build

# def market_text(self):
#     stone_player = str(resource[str(self.message_chat_id)]["stone"])
#     wood_player = str(resource[str(self.message_chat_id)]["wood"])
#     iron_player = str(resource[str(self.message_chat_id)]["iron"])
#     food_player = str(resource[str(self.message_chat_id)]["food"])
#     gold_player = str(resource[str(self.message_chat_id)]["gold"])
#     text = texting.text_building_market % (gold_player, stone_player, wood_player, iron_player, food_player)
#     return text
#
# def keyboard_market(self):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.add(telebot.types.InlineKeyboardButton(text="💰 Купить", callback_data="build_market_buy"),
#                  telebot.types.InlineKeyboardButton(text="💰 Продать", callback_data="build_market_sell"))
#     keyboard.row(telebot.types.InlineKeyboardButton(text=texting.button_back, callback_data="build_back"))
#     return keyboard
#
# def keyboard_market_buysell(self):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     m = self.call_data.split("_")[2]
#     stone1000 = telebot.types.InlineKeyboardButton(text="⛏ Камень 1000",
#                                                    callback_data="build_market_" + m + "_stone_1000")
#     iron1000 = telebot.types.InlineKeyboardButton(text="⚒ Железо 1000",
#                                                   callback_data="build_market_" + m + "_iron_1000")
#     wood1000 = telebot.types.InlineKeyboardButton(text="🌲 Дерево 1000",
#                                                   callback_data="build_market_" + m + "_wood_1000")
#     food1000 = telebot.types.InlineKeyboardButton(text="🌽 Еда 1000",
#                                                   callback_data="build_market_" + m + "_food_1000")
#     stone10000 = telebot.types.InlineKeyboardButton(text="⛏ Камень 10000",
#                                                     callback_data="build_market_" + m + "_stone_10000")
#     iron10000 = telebot.types.InlineKeyboardButton(text="⚒ Железо 10000",
#                                                    callback_data="build_market_" + m + "_iron_10000")
#     wood10000 = telebot.types.InlineKeyboardButton(text="🌲 Дерево 10000",
#                                                    callback_data="build_market_" + m + "_wood_10000")
#     food10000 = telebot.types.InlineKeyboardButton(text="🌽 Еда 10000",
#                                                    callback_data="build_market_" + m + "_food_10000")
#
#     if m == "buy":
#         buysell = telebot.types.InlineKeyboardButton(text="Выберите кол-во для покупки", callback_data="nuu")
#     elif m == "sell":
#         buysell = telebot.types.InlineKeyboardButton(text="Выберите кол-во для продажи", callback_data="nuu")
#
#     keyboard.row(buysell)
#     keyboard.row(stone1000, stone10000)
#     keyboard.row(wood1000, wood10000)
#     keyboard.row(iron1000, iron10000)
#     if m == "buy":
#         keyboard.row(food1000, food10000)
#
#     keyboard.row(telebot.types.InlineKeyboardButton(text=texting.button_back, callback_data="build_market_null"))
#     return keyboard

# def buysell(self):
#
#     m = self.call_data.split("_")[2]
#     res = self.call_data.split("_")[3]
#     num = int(self.call_data.split("_")[4])
#     lvl_storage = build[str(self.message_chat_id)]["storage"]
#     #        print(lvl_storage)
#     if m == "buy":
#         if resource[str(self.message_chat_id)]["gold"] - int(num / 100) < 0:
#             bot.answer_callback_query(callback_query_id=call.id, text="У вас не хватает золота")
#         elif resource[str(self.message_chat_id)][res] + num > buildings["storage"][lvl_storage]["capacity"]:
#             bot.answer_callback_query(callback_query_id=call.id, text="Нет места на складе")
#         else:
#             resource[str(self.message_chat_id)]["gold"] -= int(num / 100)
#             resource[str(self.message_chat_id)][res] += num
#             bot.edit_message_text(text=self.market_text(), chat_id=self.message_chat_id,
#                                   message_id=self.call_message_id,
#                                   reply_markup=self.keyboard_market_buysell())
#     elif m == "sell":
#         if resource[str(self.message_chat_id)][res] - num < 0:
#             bot.answer_callback_query(callback_query_id=call.id, text="У вас не хватает ресурсов")
#
#         else:
#             resource[str(self.message_chat_id)]["gold"] += int(num / 100)
#             resource[str(self.message_chat_id)][res] -= num
#             bot.edit_message_text(text=self.market_text(), chat_id=self.message_chat_id,
#                                   message_id=self.call_message_id,
#                                   reply_markup=self.keyboard_market_buysell())
#     save("resource")
