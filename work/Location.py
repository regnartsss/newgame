from text.texting import text_location_all
from utils.sql import sql_select, sql_insert
from aiogram import types
from filters.loc import send_troops_cb, send_war_cb

ava = {'stable': '🐴', 'barracks': '⚔', 'shooting': '🏹'}


async def number_warrior(user_id):
    text = text_location_all
    request = f"SELECT lvl, barracks, shooting, stable FROM warrior WHERE user_id = {user_id}"
    rows = await sql_select(request)
    for row in rows:
        text += f"{row[0]} ⚔{row[1]} 🏹{row[2]} 🐴{row[3]} \n"
    return text


async def siege_tower_number(user_id):
    text = "В башне:\n"
    request = f"SELECT lvl, barracks, shooting, stable  FROM siege_tower WHERE user_id = {user_id}"
    rows = await sql_select(request)
    if rows == []:
        await warrior_user(user_id)
        return "Нет войск\n"
    else:
        for row in rows:
            text += f"{row[0]} ⚔{row[1]} 🏹{row[2]} 🐴{row[3]} \n"
        return text


async def warrior_user(user_id):
    i = 1
    while i <= 5:
        await sql_insert(f"INSERT INTO siege_tower VALUES ({user_id}, {i},0,0,0)")
        i += 1


async def send_war(callback_data, user_id):
    war = callback_data["war"]
    lvl = callback_data["lvl"]
    num = callback_data["number"]
    request = f"""UPDATE warrior SET {war}={war}-{num} WHERE user_id = {user_id} AND lvl = {lvl}"""
    await sql_insert(request)
    request = f"""UPDATE siege_tower SET {war}={war}+{num} WHERE user_id = {user_id} AND lvl = {lvl}"""
    await sql_insert(request)
    avatar = ava[war]
    return f"\n🚶‍♂️Отправлено {avatar} {num} 🏅{lvl} лвл"


async def keyboard_location_war(callback):
    keyboard = types.InlineKeyboardMarkup()
    war = callback["war"]
    lvl = callback["lvl"]
    num = callback["number"]
    avatar = ava[war]
    number_5 = int(int(num) / 5)
    number_3 = int(int(num) / 3)
    number_2 = int(int(num) / 2)
    number_1 = int(num)
    text5 = types.InlineKeyboardButton(text=f"{avatar}{number_5}",
                                       callback_data=send_war_cb.new(war=war, lvl=lvl, number=number_5))
    text3 = types.InlineKeyboardButton(text=f"{avatar}{number_3}",
                                       callback_data=send_war_cb.new(war=war, lvl=lvl, number=number_3))
    text2 = types.InlineKeyboardButton(text=f"{avatar}{number_2}",
                                       callback_data=send_war_cb.new(war=war, lvl=lvl, number=number_2))
    text1 = types.InlineKeyboardButton(text=f"{avatar}{number_1}",
                                       callback_data=send_war_cb.new(war=war, lvl=lvl, number=number_1))
    keyboard.row(text5, text3, text2, text1)
    keyboard.row(types.InlineKeyboardButton(text="Назад", callback_data="tower_main_menu"))
    return keyboard


async def keyboard_location(user_id):

    keyboard = types.InlineKeyboardMarkup()
    request = f"SELECT lvl, barracks, shooting, stable FROM warrior WHERE user_id = {user_id}"
    rows = await sql_select(request)
    for row in rows:
        barr_text = f"⚔ {row[0]} лвл {row[1]}"
        shoot_text = f"🏹 {row[0]} лвл {row[2]}"
        stable_text = f"🐴 {row[0]} лвл {row[3]}"
        barr = types.InlineKeyboardButton(text=barr_text,
                                          callback_data=send_troops_cb.new(war="barracks", lvl=row[0], number=row[1]))
        shoot = types.InlineKeyboardButton(text=shoot_text,
                                           callback_data=send_troops_cb.new(war="shooting", lvl=row[0], number=row[2]))
        stable = types.InlineKeyboardButton(text=stable_text, callback_data=send_troops_cb.new(war="stable", lvl=row[0], number=row[3]))
        keyboard.row(barr, shoot, stable)
    return keyboard
