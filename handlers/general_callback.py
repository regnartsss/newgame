from loader import dp, bot
from aiogram import types
from work.Build import build, keyboard_market, keyboard_market_buysell
from work.Fight import fight, field_goto
from work.Training import entry, training, train
from work.Buy import buy_check_qiwi
from work.BattleCastle import Castle
from keyboards.keyboard import keyboard_buy


@dp.callback_query_handler(text='null')
async def market(call: types.CallbackQuery):
    await call.answer(text="")


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'buy_qiwi')
async def handler(call: types.CallbackQuery):
    await call.message.answer(text=await buy_check_qiwi(call.message))


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'buy')
async def handler(call: types.CallbackQuery):
    await call.message.answer(text="Выберите платежную систему", reply_markup=keyboard_buy())


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'null')
async def handler(call: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'fight')
async def handler(call: types.CallbackQuery):
    await fight(message=call.message, call=call)


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'entry')
async def handler(call: types.CallbackQuery):
    await entry(call=call)


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'training')
async def handler(call: types.CallbackQuery):
    await training(call=call)


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'train')
async def handler(call: types.CallbackQuery):
    await train(call=call)




@dp.callback_query_handler(lambda call: call.data == 'battle')
async def handler(call: types.CallbackQuery):
    print(f"PASS_{call.data}")
    pass


@dp.callback_query_handler(lambda call: call.data == 'field')
async def handler(call: types.CallbackQuery):
    await field_goto(call)





