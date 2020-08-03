from loader import dp, storage
from aiogram import types
from text.texting import button_location
from work.Location import number_warrior, siege_tower_number, keyboard_location, keyboard_location_war, send_war
from keyboards.keyboard import keyboard_locat
from middlewares.middl_time import time_start
from filters.loc import send_troops_cb, send_war_cb


@dp.message_handler(text=button_location)
@time_start()
async def stop(message: types.Message):
    text = await number_warrior(message.from_user.id)
    await message.answer(text=text, reply_markup=keyboard_locat())


@dp.message_handler(text="🗼 Осада башни")
@time_start()
async def stop(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id + 1})
    await message.answer(text=await siege_tower_number(user_id), reply_markup=await keyboard_location(user_id))


@dp.callback_query_handler(text="tower_main_menu")
async def market(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.edit_text(text=await siege_tower_number(user_id), reply_markup=await keyboard_location(user_id))


@dp.callback_query_handler(send_troops_cb.filter(number='0'))
async def market(call: types.CallbackQuery):
    await call.answer("У вас нет этих войск")


@dp.callback_query_handler(send_troops_cb.filter(war=["barracks", "shooting", "stable"]))
async def market(call: types.CallbackQuery, callback_data: dict):
    text = "Выберите количество воинов"
    await call.message.edit_text(text=text, reply_markup=await keyboard_location_war(callback_data))


@dp.callback_query_handler(send_war_cb.filter(war=["barracks", "shooting", "stable"]))
async def market(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    text = await siege_tower_number(user_id)
    text += await send_war(callback_data, user_id)
    await call.message.edit_text(text=text, reply_markup=await keyboard_location(user_id))
