from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from utils import sql
from text import texting
from keyboards import keyboard
from work import Fight, Shop, Top
from work import Build, Map, Users, Training
from data.config import admins
import importlib
from middlewares.middleware_and_antiflood import rate_limit
from work.BattleCastle import Castle
from work.Buy import function_buy, Buy



async def reload_module():
    importlib.reload(texting)
    importlib.reload(keyboard)
    importlib.reload(Map)
    importlib.reload(Build)
    importlib.reload(Fight)
    importlib.reload(Users)
    importlib.reload(Shop)
    importlib.reload(Training)


@dp.message_handler(state=Users.NewName.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    await sql.sql_insert("UPDATE heroes SET nik_name = '%s' WHERE user_id = %s" % (message.text, message.chat.id))
    await message.answer(text=texting.text_main_menu % message.text, reply_markup=keyboard.keyboard_main_menu())


@dp.message_handler(state=Shop.Form.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "11":
        await message.answer("Отмена")
        await state.finish()
    else:
        await Shop.shop_rename_heroes_win(message)


@dp.message_handler(state=Shop.Form.coordinates)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "11":
        await message.answer("Отмена")
        await state.finish()
    else:
        if await Shop.moving_heroes_win(message) is True:
            await state.finish()


@dp.message_handler(state=Buy.amount)
async def process_name(message: types.Message, state: FSMContext):
    await function_buy(message, state)





@dp.message_handler(content_types=types.ContentTypes.TEXT)
@rate_limit(0.5)
async def all_other_messages(message: types.Message):
    if message.chat.id in admins:
        if message.text == "reload":
            await reload_module()
            await message.answer("Модули обновлены")


    if "f" == 1:
        pass
        # print("Бот остановлен")
        # await message.answer("Бот временно остановлен")
    else:
        data_old = await sql.sql_selectone("select message_id from heroes where user_id = %s" % message.chat.id)
        if data_old[0] != 0:
            try:
                print("Надо удалить")
                await bot.delete_message(message.chat.id, data_old[0])
            except Exception as n:
                print("Не чего удалять %s" % n)
            await sql.sql_insert("update heroes set message_id = 0 where user_id = %s" % message.chat.id)

        if message.text in texting.list_Maps:
            await sql.sql_insert(
                "update heroes set message_id = %s where user_id = %s" % (message.message_id + 2, message.chat.id))
            if message.text == texting.button_goto or message.text == texting.button_goto_two:
                print("оступить")
                request = f"""delete from battle_enemy where user_id == {message.chat.id};
                                delete from combinations where user_id = {message.chat.id};
                                
                            """
                await sql.sql_insertscript(request)
                await bot.send_message(text="⏱ Вывод карты ⏱", chat_id=message.chat.id,
                                       reply_markup=keyboard.keyboardmap())
                await Map.goto(message=message, call=" ")
            # Вернуться на карту
            elif message.text == texting.button_mining_map:
                await Map.timer_mining(message, "stop")
            elif message.text == texting.button_castle_escape or message.text == texting.button_castle_escape_field:
                 print("asdasd")
                 await Castle(message=message, call="").castle_escape()
                 await sql.sql_insert(
                     "update heroes set message_id = %s where user_id = %s" % (message.message_id + 2, message.chat.id))

                 # await bot.send_message(text="⏱ Вывод карты ⏱", chat_id=message.chat.id,
                 #                        reply_markup=keyboard.keyboardmap())
                 await Map.goto(message=message, call=" ")

            # elif message.text == texting.button_goto:
            #     Fight(message=message).fight()
            else:
                # users[str(message.chat.id)]["mess_id"] = message.message_id + 2
                await bot.send_message(text="⏱ Вывод карты ⏱", chat_id=message.chat.id,
                                       reply_markup=keyboard.keyboardmap())
                await Map.goto(message=message, call=" ")
        # Домой
        elif message.text == texting.button_castle:
            await bot.send_message(text="🏘 Домой", chat_id=message.chat.id, reply_markup=keyboard.keyboard_main_menu())
        # Копать
        elif message.text == texting.button_mining:
            await Map.timer_mining(message, "start")

        elif message.text == texting.button_mining_ataka:
            await message.answer(text=texting.text_mining_ataka, reply_markup=keyboard.keyboard_map())
            await Fight.mining_attack(message)
        # Назад
        elif message.text == texting.button_back:
            await bot.send_message(text=texting.button_back, chat_id=message.chat.id,
                                   reply_markup=keyboard.keyboard_main_menu())
        # Инфо герой
        elif message.text == texting.button_heroes:
            await Users.info_heroes(message)
            # await message.answer(text=Users.info_heroes(message, key))
            # await message.answer(text=Users.info_heroes(message, key="build"))
        # Атаковать
        elif message.text == texting.button_attack:
            await Fight.fight(message=message, call='')
        # Cтроение
        elif message.text == texting.button_building:
            menu = "building"
            await sql.sql_insert(
                "update heroes set message_id = %s where user_id = %s" % (message.message_id + 1, message.chat.id))
            await Build.building(message=message)
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
            await bot.send_message(text="Выберите платежную систему", chat_id=message.chat.id,
                                   reply_markup=keyboard.keyboard_buy())
        # elif message.text == "Tranzzo":
        #     menu = "Tranzzo"
        #     buy.buy_amount(message)
        elif message.text == texting.button_start:
            await Users.start_user_name(message)
        elif message.text == "💬 Чат":
            await bot.send_message(message.chat.id,
                                   "Чат предназначен для общения, предложения идей и выявления багов @heroeslifeg")
        elif message.text == "Пригласить":
            bot_username = (await bot.me).username
            bot_link = f"https://t.me/{bot_username}?start={message.chat.id}"
            await message.answer("Для приглашения друга отправть ему ссылку ниже. \n"
                                 "И получи 💎 за каждый взятый им уровень")
            await message.answer(bot_link)
        elif message.text == texting.button_help:
            pass
        #        help(message)
        # elif message.text == texting.button_location:
        #     menu = "Location"
        #     Location(message=message).keyboard_warrior()
        # elif message.text == "🗼 Осада башни":
        #     Location(message=message).location()

        # elif message.text == 'Общий рейтинг за башни':
        #     statisctick(message, "all")
        # elif message.text == 'Последний бой за башни':
        #     statisctick(message, "one")
        # elif message.text == "Время":
        #     test()
        # Магазин
        elif message.text == texting.button_shop:
            await message.answer(text="Для подробной информации о товаре, нажмите на него",
                                 reply_markup=Shop.keyboard_shop())
        elif message.text == "Создать карту":
            await Map.new_maps()
        elif message.text == texting.button_top:
            await message.answer(text=texting.button_top, reply_markup=keyboard.keyboard_statisctick())
        elif message.text == texting.button_top_heroes:
            await message.answer(text=await Top.top_heroes(message))
        elif message.text == texting.button_top_castle:
            await message.answer(text=await Top.top_castle(message))

        #
        elif message.text == texting.button_castle_attack:
            await sql.sql_insert(
                "update heroes set message_id = %s where user_id = %s" % (message.message_id + 3, message.chat.id))
            # users[str(message.chat.id)]["mess_id"] = message.message_id + 1
            await Castle(message, call="").castle_pole()
        # elif message.text == texting.button_castle_escape_field:
        #     Castle(message).castle_escape_field()
        else:
            print(message.text)
