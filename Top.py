import sql
from texting import text_top_castle, text_top_heroes


async def top_heroes(message):
    request = f"SELECT avatar, nik_name, lvlheroes, user_id FROM heroes ORDER BY lvlheroes DESC LIMIT 10"
    rows = await sql.sql_select(request)
    text = text_top_heroes
    i, stop = 1, 0
    for row in rows:
        if row[3] == message.chat.id:
            stop = 1
        text += f"{i}) {row[0]} {row[1]} - {row[2]} ур.\n"
        i += 1
    if stop == 0:
        rows = await sql.sql_select("SELECT avatar, nik_name, lvlheroes, user_id FROM heroes ORDER BY lvlheroes DESC")
        y = 1
        for row in rows:
            if row[3]== message.chat.id:
                text += "--------------------\n"
                text += f"{y}) {row[0]} {row[1]} - {row[2]} ур.\n"
            y += 1
    return text


async def top_castle(message):
    request = f"SELECT avatar, nik_name, castle, user_id FROM heroes ORDER BY castle DESC LIMIT 10"
    rows = await sql.sql_select(request)
    text = text_top_castle
    i, stop = 1, 0
    for row in rows:
        if row[3] == message.chat.id:
            stop = 1
        text += f"{i}) {row[0]} {row[1]} - {row[2]} ур.\n"
        i += 1
    if stop == 0:
        rows = await sql.sql_select("SELECT avatar, nik_name, lvlheroes, user_id FROM heroes ORDER BY castle DESC")
        y = 1
        for row in rows:
            if row[3]== message.chat.id:
                text += "--------------------\n"
                text += f"{y}) {row[0]} {row[1]} - {row[2]} ур.\n"
            y += 1
    return text