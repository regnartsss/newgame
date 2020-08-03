from loader import dp, storage
from aiogram import types
from text.texting import button_goto, button_goto_two, button_castle_escape, button_castle_escape_field
from text.texting import button_maps, button_mining_map, button_mining, text_mining_start
from keyboards.keyboard import keyboardmap, keyboard_map
from work.Map import goto, timer_mining
from work.BattleCastle import Castle
from utils.sql import sql_insertscript


@dp.message_handler(text=[button_goto, button_goto_two])    # Сбежать, Отступить
async def maps(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id + 2})
    request = f"""
                        delete from battle_enemy where user_id == {user_id};
                        delete from combinations where user_id = {user_id};
                       """
    await sql_insertscript(request)
    await message.answer(text="⏱ Вывод карты ⏱", reply_markup=keyboardmap())
    await goto(message=message, call=" ")


@dp.message_handler(text=[button_castle_escape, button_castle_escape_field])    # Покинуть поле боя
async def maps(message: types.Message):
    user_id = message.from_user.id
    await Castle(message=message, call="").castle_escape()
    await storage.set_data(chat=user_id, data={"message_id": message.message_id + 2})
    await message.answer(text="⏱ Вывод карты ⏱", reply_markup=keyboardmap())
    await goto(message=message, call=" ")


@dp.message_handler(text=[button_maps, button_mining_map])
async def maps(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id + 2})
    await message.answer(text="⏱ Вывод карты ⏱", reply_markup=keyboardmap())
    await goto(message=message, call=" ")


@dp.message_handler(text=button_mining)
async def star(message: types.Message):
    await timer_mining(message, "start")
    await message.answer(text=text_mining_start, reply_markup=keyboard_map())


@dp.message_handler(text=button_mining_map)
async def stop(message: types.Message):
    text = await timer_mining(message, "stop")
    await message.answer(text=text, reply_markup=keyboardmap())
    await goto(call="*", message=message)


@dp.callback_query_handler(lambda callback_query: True)
async def handler(call: types.CallbackQuery):
    print(f"Неверная call {call.data.split('_')[:2]}")
    await goto(call=call, message=call.message)
