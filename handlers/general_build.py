from loader import dp, bot, storage
from aiogram import types
from work.Build import build, keyboard_market, keyboard_market_buysell, buysell, market_text, keyboard_building
from text.texting import text_building_update, button_building
from work.Users import info_heroes



@dp.callback_query_handler(text='build_market_null')
async def market(call: types.CallbackQuery):
    text = await market_text(call.from_user.id)
    keyboard = await keyboard_market()
    await call.message.edit_text(text=text, reply_markup=keyboard)


@dp.callback_query_handler(text='build_market_buy')
async def market(call: types.CallbackQuery):
    keyboard = await keyboard_market_buysell(call.data.split("_")[2])
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text='build_market_sell')
async def market(call: types.CallbackQuery):
    keyboard = await keyboard_market_buysell(call.data.split("_")[2])
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(lambda call: '_'.join(call.data.split("_")[:3]) == 'build_market_sell')
async def market(call: types.CallbackQuery):
    await buysell(call)


@dp.callback_query_handler(lambda call: '_'.join(call.data.split("_")[:3]) == 'build_market_buy')
async def market(call: types.CallbackQuery):
    await buysell(call)


@dp.callback_query_handler(text='build_back')
async def handler(call: types.CallbackQuery):
    text = text_building_update % (await info_heroes(call.message, key="build"))
    await call.message.edit_text(text=text, reply_markup=await keyboard_building(call.from_user.id))


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'build')
async def handler(call: types.CallbackQuery):
    print(call.data)
    await build(message=call.message, call=call)


@dp.message_handler(text=button_building)   # Строения
async def stop(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id+1})
    text = text_building_update % (await info_heroes(message, key="build"))
    await message.answer(text=text, reply_markup=await keyboard_building(message.from_user.id))
