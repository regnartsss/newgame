from aiogram import types
from loader import bot
from text.texting import text_training_castle, text_training_uplvl, text_training_numwar, text_training_castle_old
from utils import sql


async def training(call):
    old = call.data.split("_")[1]
    lvl = call.data.split("_")[2]
    status = call.data.split("_")[3]
    if status == "⛔":
        await bot.answer_callback_query(callback_query_id=call.id, text=text_training_uplvl)
    else:
        text = await text_training(call) + text_training_numwar
        try:
            await call.message.edit_text(text=text, reply_markup=await keyboard_training_one(call))
        except Exception as n:
            print(f"ERROR_1 {n}")


async def entry(call):
    text = await text_training(call) + "\n Выберите уровень войск"
    try:
        await call.message.edit_text(text=text, reply_markup=await keyboard_training_lvl(call))
    except Exception as n:
        print(f"ERROR_2 {n}")


async def train(call):
    name = call.data.split("_")[1]
    lvl = call.data.split("_")[2]
    number = int(call.data.split("_")[3])
    status = call.data.split("_")[4]
    if status == "✅":
        request = f"SELECT wood, stone, iron, food FROM training Where name = '{name}' and lvl = {lvl}"
        wood, stone, iron, food = await sql.sql_selectone(request)
        wood *= number
        stone *= number
        iron *= number
        food *= number
        request = f"""UPDATE resource SET wood = wood - {wood}, 
                                              stone = stone - {stone}, 
                                              iron = iron - {iron}, 
                                              food = food - {food}
                                WHERE user_id = {call.message.chat.id};
                        UPDATE warrior SET {name} = {name} + {number} 
                            WHERE user_id = {call.message.chat.id} and lvl = {lvl}"""

        await sql.sql_insertscript(request)
        await bot.answer_callback_query(callback_query_id=call.id, text="Обучение успешно")
        await call.message.edit_text(text=await text_training(call), reply_markup=await keyboard_training_one(call))
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Не хватает ресурсов")


async def keyboard_training_one(call):
    name = call.data.split("_")[1]
    lvl = call.data.split("_")[2]
    keyboard = types.InlineKeyboardMarkup()
    number = [5, 10, 25, 50]
    request = f"SELECT avatar, wood, stone, iron, food, consumption FROM training Where name = '{name}' and lvl = {lvl}"
    row = await sql.sql_selectone(request)
    for i in number:
        lvl_heroes = (await sql.sql_selectone(f"Select lvlheroes FROM heroes WHERE user_id = {call.message.chat.id}"))[
            0]
        num = lvl_heroes * i
        row_user = await sql.sql_selectone(
            f"SELECT wood, stone, iron, food FROM resource WHERE user_id = {call.message.chat.id}")
        if row[1] * num > row_user[0] or row[2] * num > row_user[1] or row[3] * num > row_user[2] or row[4] * num > \
                row_user[3]:
            status = "⛔"
        else:
            status = "✅"
        wood = number_thousand(row[1] * num)
        stone = number_thousand(row[2] * num)
        iron = number_thousand(row[3] * num)
        food = number_thousand(row[4] * num)
        cons = number_thousand(row[5] * num)
        text = f"""{status} {num} {row[0]} 🌲{wood} ⛏{stone} ⚒{iron} 🌽{food} / -🌽{cons}/мин."""
        keyboard.row(types.InlineKeyboardButton(text=text, callback_data=f"train_{name}_{lvl}_{num}_{status}"))
    keyboard.row(types.InlineKeyboardButton(text="Назад", callback_data=f"entry_{name}"))
    return keyboard


def number_thousand(num):
    num = int(num)
    if num < 1000:
        return f"{num} "
    else:
        return f"{int(num / 1000)}т. "


async def keyboard_training_lvl(call):
    name = call.data.split("_")[1]
    keyboard = types.InlineKeyboardMarkup()
    # number = [1, 2, 3, 4, 5]
    request = f"SELECT avatar, wood, stone, iron, food, consumption FROM training Where name = '{name}'"
    building = (await sql.sql_selectone(f"SELECT {name} FROM heroes Where user_id = '{call.message.chat.id}'"))[0]
    rows = await sql.sql_select(request)
    i = 1
    for row in rows:
        if building < i * 4:
            status = "⛔"
        else:
            status = "✅"
        text = f"{status} {row[0]} {i} лвл /  🌲 {row[1]} ⛏ {row[2]} ⚒ {row[3]} 🌽 {row[4]} / -🌽 {row[5]}"
        keyboard.row(types.InlineKeyboardButton(text=text, callback_data=f"training_{name}_{i}_{status}"))
        i += 1
    keyboard.row(types.InlineKeyboardButton(text="Назад", callback_data="build_" + name))
    return keyboard


async def text_training(call):
    name = call.data.split("_")[1]
    text = text_training_castle
    request = f"""SELECT avatar, consumption, {name} FROM training INNER JOIN warrior   
                                ON training.lvl = warrior.lvl  
                                WHERE user_id = {call.message.chat.id} AND name = '{name}'"""
    print(request)
    rows = await sql.sql_select(request)
    print(rows)
    num = 1
    for row in rows:
        text += text_training_castle_old % (row[0], row[2], num, row[1] * row[2])
        num += 1
    return text
