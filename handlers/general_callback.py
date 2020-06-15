from loader import dp, bot
from aiogram import types
from work.Map import goto
from work.Build import build
from work.Fight import fight, field_goto
from work.Training import entry
from utils import sql
from work.Shop import shop
from work.Buy import buy_amount
from work.BattleCastle import Castle
from keyboards.keyboard import keyboard_buy_cancel
#
# @dp.callback_query_handler()
# async def handler(call: types.CallbackQuery):


@dp.callback_query_handler(lambda callback_query: True)
async def handler(call: types.CallbackQuery):
    # print(call.message.from_user.id)
    if (await sql.sql_selectone("select start_bot from data"))[0] == 1:
        print("Бот остановлен")
        await call.message.answer("Бот временно остановлен")
    else:
        print("Игрок %s - %s" % (call.message.chat.id, call.data))
        # list_castle = ["start", "step", "castle", "hit"]
        #   buy_bot = Buy(message=call.message, call=call)
        if call.data == "null" or call.data == "1":
            await bot.answer_callback_query(callback_query_id=call.id)
        elif call.data.split("_")[0] == "battle":
            pass
        elif call.data.split("_")[0] == "build":
            await build(message=call.message, call=call)
        elif call.data.split("_")[0] == "fight":
            await fight(message=call.message, call=call)

        # #   elif call.data == "buy_qiwi":
        # #       buy_bot.buy_check_qiwi()
        # elif call.data == "null":
        #     bot.answer_callback_query(callback_query_id=call.id, text='Не активное поле')
        #    elif call.data.split("_")[0] == "help":
        #        help(message=call.message, call=call)
        #    elif call.data.split("_")[0] == "gotobattle":
        #        all_battle()
        elif call.data.split("_")[0] == "entry":
            # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await entry(message=call.message, call=call)
        elif call.data.split("_")[0] == "training":
            await entry(message=call.message, call=call)
        elif call.data.split("_")[0] == "train":
            await entry(message=call.message, call=call)
        # elif call.data.split("_")[0] == "tower" or call.data.split("_")[0] == "towerold":
        #     Location(message=call.message, call=call).location()
        elif call.data.split("_")[0] == "shop":
            await shop(call=call)
        elif call.data.split("_")[0] == "field":
            await field_goto(call)
        elif call.data.split("_")[0] == "buy":
            # await field_goto(call)
            # await call.message.edit_reply_markup(reply_markup=keyboard_buy_cancel)
            await buy_amount(call)
        # # battle_castle
        elif call.data.split("_")[0] == "castle":
            await Castle(call=call, message=call.message).castle_pole_timer()
        elif call.data == "step_break":
            await Castle(call=call, message=call.message).castle_pole_break()
        elif call.data == "step_null":
            await bot.answer_callback_query(callback_query_id=call.id, text="Ожидайте соперника")
        elif call.data == "step_field":
            await bot.answer_callback_query(callback_query_id=call.id, text="Пустое поле")
        elif call.data.split("_")[0] == "step":
            await Castle(call=call, message=call.message).castle_pole_step()
        elif call.data.split("_")[0] == "hit":
            await Castle(call=call, message=call.message).castle_pole_hit()
        else:
            await goto(message=call.message, call=call)




