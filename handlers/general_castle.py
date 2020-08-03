from loader import dp, storage
from aiogram import types
from work.BattleCastle import Castle
from text.texting import button_castle_attack


@dp.callback_query_handler(text='castle')
async def handler(call: types.CallbackQuery):
    await Castle(call=call, message=call.message).castle_pole_timer()


@dp.callback_query_handler(text='step_break')
async def handler(call: types.CallbackQuery):
    await Castle(call=call, message=call.message).castle_pole_break()


@dp.callback_query_handler(text='step_null')
async def handler(call: types.CallbackQuery):
    await call.answer(text="Ожидайте соперника")


@dp.callback_query_handler(text='step_field')
async def handler(call: types.CallbackQuery):
    await call.answer(text="Пустое поле")


@dp.callback_query_handler(text='step')
async def handler(call: types.CallbackQuery):
    await Castle(call=call, message=call.message).castle_pole_step()


@dp.callback_query_handler(text='hit')
async def handler(call: types.CallbackQuery):
    await Castle(call=call, message=call.message).castle_pole_hit()


@dp.message_handler(text=button_castle_attack)
async def top_castle(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id + 3})
    await Castle(message, call="").castle_pole()
