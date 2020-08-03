from aiogram import types
from loader import dp, bot, storage
from aiogram.dispatcher import FSMContext
from utils import sql
from text import texting
from text.buy import textsell
from keyboards import keyboard
from work import Build, Users, Training, Fight, Top
# from work.BattleCastle import Castle
from work.Buy import function_buy, Buy, buy_qiwi, buy_amount
from work.Map import new_maps
from data.config import admins
from work.BattleTower import start_battle_tower


def reload_module_text():
    import importlib
    importlib.reload(texting)
    print(texting.test)
    importlib.reload(keyboard)
    importlib.reload(Build)
    importlib.reload(Fight)
    importlib.reload(Users)
    importlib.reload(Training)


@dp.message_handler(lambda c: c.from_user.id in admins)
async def admin(message: types.Message):
    print(message.text)
    user_id = message.from_user.id
    if message.text == "reload":
        reload_module_text()
        await message.answer("Модули обновлены")
        print(texting.test)
    elif message.text == "111":
        await storage.set_data(chat=user_id, data={"message_id": message.message_id + 1})
    elif message.text == "222":
        await start_battle_tower()


@dp.message_handler(state=Users.NewName.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    await sql.sql_insert("UPDATE heroes SET nik_name = '%s' WHERE user_id = %s" % (message.text, message.chat.id))
    await message.answer(text=texting.text_main_menu % message.text, reply_markup=keyboard.keyboard_main_menu())


@dp.message_handler(state=Buy.amount)
async def process_name(message: types.Message, state: FSMContext):
    await function_buy(message, state)


@dp.message_handler(text=texting.button_heroes)
async def info(message: types.Message):
    await message.answer(text=await Users.info_heroes(message))


@dp.message_handler(text=texting.button_castle)
async def stop(message: types.Message):
    await message.answer(text="🏘 Домой", reply_markup=keyboard.keyboard_main_menu())


@dp.message_handler(text=texting.button_mining_ataka)
async def stop(message: types.Message):
    await message.answer(text=texting.text_mining_ataka, reply_markup=keyboard.keyboard_map())
    await Fight.mining_attack(message)


@dp.message_handler(text=texting.button_location)
async def stop(message: types.Message):
    pass
    # Location(message=message).keyboard_warrior()


@dp.message_handler(text=texting.button_back)
async def back(message: types.Message):
    await message.answer(text=texting.button_back, reply_markup=keyboard.keyboard_main_menu())


@dp.message_handler(text=texting.button_buy_cancel)
async def buy_cancel(message: types.Message):
    await message.answer(texting.button_buy_cancel, reply_markup=keyboard.keyboard_main_menu())


@dp.message_handler(text=texting.button_top)
async def top_heroes(message: types.Message):
    await message.answer(text=texting.button_top, reply_markup=keyboard.keyboard_statisctick())


@dp.message_handler(text=texting.button_top_heroes)
async def top_heroes(message: types.Message):
    await message.answer(text=await Top.top_heroes(message))


@dp.message_handler(text=texting.button_top_castle)
async def top_castle(message: types.Message):
    await message.answer(text=await Top.top_castle(message))


@dp.message_handler(text="Пригласить")
async def top_castle(message: types.Message):
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={message.chat.id}"
    await message.answer("Для приглашения друга отправть ему ссылку ниже. \n"
                         "И получи 💎 за каждый взятый им уровень")
    await message.answer(bot_link)


@dp.message_handler(text=texting.button_attack)
async def top_castle(message: types.Message):
    await Fight.fight(message=message, call='')

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def all_other_messages(message: types.Message):
    print("ff")
    if "f" == 1:
        pass
        # print("Бот остановлен")
        # await message.answer("Бот временно остановлен")
    else:
        data_old = await sql.sql_selectone("select message_id from heroes where user_id = %s" % message.chat.id)
        # if data_old[0] != 0:
        #     try:
        #         print("Надо удалить")
        #         await bot.delete_message(message.chat.id, data_old[0])
        #     except Exception as n:
        #         print("Не чего удалять %s" % n)
        #     await sql.sql_insert("update heroes set message_id = 0 where user_id = %s" % message.chat.id)

        if message.text in texting.list_Maps:
            pass
        # Домой
        # elif message.text == texting.button_castle:
        #     await bot.send_message(text="🏘 Домой", chat_id=message.chat.id, reply_markup=keyboard.keyboard_main_menu())
        # Копать
        # elif message.text == texting.button_mining:
        #     await Map.timer_mining(message, "start")

        # elif message.text == texting.button_mining_ataka:
        #     await message.answer(text=texting.text_mining_ataka, reply_markup=keyboard.keyboard_map())
        #     await Fight.mining_attack(message)
        # Назад

        # Инфо герой
        # elif message.text == texting.button_heroes:
        #     await Users.info_heroes(message)
            # await message.answer(text=Users.info_heroes(message, key))
            # await message.answer(text=Users.info_heroes(message, key="build"))
        # Атаковать

        # Cтроение
        # elif message.text == texting.button_building:
        #     menu = "building"
        #     await sql.sql_insert(
        #         "update heroes set message_id = %s where user_id = %s" % (message.message_id + 1, message.chat.id))
        #     await Build.building(message=message)
        elif message.text == texting.button_setting:
            menu = "info"
            await bot.send_message(text=texting.text_setting, chat_id=message.chat.id,
                                   reply_markup=keyboard.keyboard_info())
        elif message.text == "Обратная связь":
            menu = "feedback"
            await bot.send_message(
                text="Напишите ваши пожелания или найденные ошибки. \n Если нажали случайно, введите 'нет'",
                chat_id=message.chat.id, reply_markup=keyboard.keyboard_info())
            # bot.register_next_step_handler(message, please)
        elif message.text == "Помочь проекту":
            menu = "feedback"
            await message.answer(text="Выберите платежную систему", reply_markup=keyboard.keyboard_buy())
        # elif message.text == "Tranzzo":
        #     menu = "Tranzzo"
        #     buy.buy_amount(message)
        elif message.text == "QIWI":
            await message.answer(textsell, reply_markup=keyboard.keyboard_buy_cancel())
            await Buy.amount.set()
            # await buy_amount(message)
            # await message.answer(text="Для оплаты перейдите по ссылке", reply_markup=await buy_qiwi(message))

        elif message.text == texting.button_start:
            await Users.start_user_name(message)
        elif message.text == "💬 Чат":
            await bot.send_message(message.chat.id,
                                   "Чат предназначен для общения, предложения идей и выявления багов @heroeslifeg")

        # elif message.text == texting.button_help:
        #     pass
        #     help(message)


        # elif message.text == "🗼 Осада башни":
        #     Location(message=message).location()

        # elif message.text == 'Общий рейтинг за башни':
        #     statisctick(message, "all")
        # elif message.text == 'Последний бой за башни':
        #     statisctick(message, "one")
        # elif message.text == "Время":
        #     test()
        # Магазин

        elif message.text == "Создать карту":
            await message.answer(text=await new_maps())


        # elif message.text == texting.button_castle_escape_field:
        #     Castle(message).castle_escape_field()
        else:
            print(message.text)
