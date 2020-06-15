from aiogram import types
from text.texting import text_rename_nik, text_moving_win, text_moving_error, text_moving_busy, \
    text_moving_heroes, text_rename_nik_new, text_shop_not_diamond
from keyboards.keyboard import keyboard_main_menu
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import sql


class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    coordinates = State()  # Will be represented in storage as 'Form:age'
    # gender = State()  # Will be represented in storage as 'Form:gender'


def keyboard_shop():
    keyboard = types.InlineKeyboardMarkup()
    rename = types.InlineKeyboardButton(text="Изменить имя 5 💎", callback_data="shop_rename")
    changeavatar = types.InlineKeyboardButton(text="Изменить аватар 5 💎", callback_data="shop_avatar")
    moving = types.InlineKeyboardButton(text="Перемещение 10 💎", callback_data="shop_moving")
    sell = types.InlineKeyboardButton(text="Купить 💎", callback_data="buy_sell")
    keyboard.add(rename)
    keyboard.add(changeavatar)
    keyboard.add(moving)
    keyboard.add(sell)
    return keyboard


async def shop(call):
    if call.data.split("_")[1] == "menu":
        try:
            pass
            # bot.edit_message_text(text="Для подробной информации о товаре, нажмите на него",
            #                       chat_id=self.message_chat_id,
            #                       message_id=self.call_message_id, reply_markup=self.keyboard_shop())
        except Exception as n:
            print(f"error_shop_1 {n}")

    elif call.data.split("_")[1] == "avatar":
        await call.message.edit_text(text="Выберите аватар\n Стоимость смены аватара 5 💎", reply_markup=await avatar())
    elif call.data.split("_")[1] == "emoji":
        await shop_edit_emoji(call)
    elif call.data.split("_")[1] == "sell":
        pass
        # buy.buy_amount(message=self.message)
    elif call.data.split("_")[1] == "rename":
        await call.message.delete()
        await shop_rename_heroes(call)
    elif call.data.split("_")[1] == "moving":
        await call.message.delete()
        await moving_heroes(call)
    elif call.data.split("_")[2] == "yes":
        await shop_edit_emoji_yes(call)
    elif call.data.split("_")[2] == "no":
        await call.message.edit_text(text="Отмена", reply_markup=await avatar())


async def shop_edit_emoji(call):
    key = call.data.split("_")[2]
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="shop_" + key + "_yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data="shop_" + key + "_no")
    keyboard.row(yes, no)
    await call.message.edit_text(
        text=f"Стоимость смены аватара 5 💎.\nВы действительно хотите сменить аватар на {key} ?",
        reply_markup=keyboard)


async def shop_edit_emoji_yes(call):
    key = call.data.split("_")[1]
    diamond = (await sql.sql_selectone(f"SELECT diamond FROM resource WHERE user_id = {call.message.chat.id}"))[0]
    if int(diamond) - 5 <= 0:
        await call.message.answer(text_shop_not_diamond, reply_markup=keyboard_shop())
    else:
        request = f"""UPDATE heroes SET avatar = '{key}' WHERE user_id = {call.message.chat.id};
                        UPDATE resource SET diamond = diamond - 5 WHERE user_id = {call.message.chat.id}"""
        await sql.sql_insertscript(request)
        await call.message.answer(text=f"Вы сменили аватар на {key}. Поздавляем", )


async def shop_rename_heroes(call):
    diamond = (await sql.sql_selectone(f"SELECT diamond FROM resource WHERE user_id = {call.message.chat.id}"))[0]
    if int(diamond) - 5 <= 0:
        await call.message.answer(text_shop_not_diamond, reply_markup=keyboard_shop())
    else:
        await call.message.answer(text=text_rename_nik)
        await Form.name.set()


async def shop_rename_heroes_win(message):
    reguest = f"""UPDATE heroes SET nik_name = '{message.text}' WHERE user_id = {message.chat.id};
                    UPDATE resource SET diamond = diamond - 5 WHERE user_id = {message.chat.id}
    """
    await sql.sql_insertscript(reguest)
    await message.answer(text=text_rename_nik_new % message.text, reply_markup=keyboard_main_menu())


async def avatar():
    try:
        emoji = ["🥶", "😴", "😈", "👿", "👹", "👺", "💩", "👻", "💀", "☠", "👽", "🤖", "🎃", "😺", "😸"]
        keyboard = types.InlineKeyboardMarkup()
        i = 1
        tab = []
        for key in emoji:
            tab.append(types.InlineKeyboardButton(text=key, callback_data="shop_emoji_" + key))
            if i == 5 or i == 10 or i == 15:
                keyboard.row(*tab)
                tab = []
            i += 1
        keyboard.row(*tab)
        keyboard.row(types.InlineKeyboardButton(text="Назад", callback_data="shop_menu"))
        return keyboard
    except Exception as n:
        print(f"error_avatar {n}")


async def moving_heroes(call):
    diamond = (await sql.sql_selectone(f"SELECT diamond FROM resource WHERE user_id = {call.message.chat.id}"))[0]
    if int(diamond) - 5 <= 0:
        await call.message.answer(text_shop_not_diamond, reply_markup=keyboard_shop())
    else:
        await call.message.answer(text=text_moving_heroes)
        await Form.coordinates.set()


async def moving_heroes_win(message):
    try:
        int(message.text.split(":")[0])
        int(message.text.split(":")[1])
    except ValueError:
        await message.answer(text=text_moving_error)
        return False
    except IndexError:
        await message.answer(text=text_moving_error)
        return False
    x = int(message.text.split(":")[0])
    y = int(message.text.split(":")[1])
    if 0 < x < 100 and 0 < y < 100:
        print("прошло")
        cell = x * 100 + y
        if (await sql.sql_selectone(f"SELECT resource FROM maps WHERE maps_id = {cell}"))[0] == "null":
            request = f"""
UPDATE maps SET resource = 'null', lvl = 0, number = 0, id = 0 WHERE maps_id = 
(SELECT cell FROM heroes WHERE user_id = {message.chat.id});
UPDATE maps SET resource = 'user', lvl = 0, number = 0, id = {message.chat.id} WHERE maps_id = {cell};
UPDATE heroes SET cell = {cell} WHERE user_id = {message.chat.id};
UPDATE resource SET diamond = diamond - 10 WHERE user_id = {message.chat.id}"""
            await sql.sql_insertscript(request)
            await message.answer(text=text_moving_win % (x, y))
            return True
        else:
            await message.answer(text=text_moving_busy)

    else:
        await message.answer(text=text_moving_error)
