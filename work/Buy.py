from text.buy import textsell
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from data.config import provider_token, publicKeyQIWI
from datetime import datetime
from utils.sql import sql_insertscript, sql_insert, sql_selectone, sql_select
from keyboards.keyboard import keyboard_buy_cancel, keyboard_main_menu
from text.texting import button_buy_cancel


class Buy(StatesGroup):
    amount = State()
    us = State()


async def function_buy(message, state):
    if message.text == button_buy_cancel:
        await message.answer(button_buy_cancel, reply_markup=keyboard_main_menu())
        await state.finish()
    else:
        data = await number_check(message)
        if data == "Error_min":
            await message.answer("Повторите ввод. Минимальная покупка 1 💎")
        elif data == "Error_int":
            await message.answer("Повторите ввод. Число не корректно")
        elif data == "Ok":
            await state.finish()
            print(message.text)
            # await buy_tranzzo(message)
            await buy_qiwi(message)


async def buy_amount(message):
    print("ff")
    pass
    # if call.data == "buy_sell":
    # await message.answer(textsell, reply_markup=keyboard_buy_cancel())
    # # await bot.send_message(chat_id=call.message.chat.id, text = textsell, reply_markup=keyboard_buy_cancel())
    # await Buy.amount.set()


async def number_check(message):
    text = message.text
    try:
        print(int(text))
        if int(text) <= 0:
            return "Error_min"
        else:
            return "Ok"

    except ValueError:
        return "Error_int"

#
# async def buy_tranzzo(message):
#     amount = message.text
#     prices = [LabeledPrice(label="Heroes Life", amount=int(amount) * 1000)]
#     await bot.send_invoice(message.chat.id, title='Покупку алмазов в Heroes Life',
#                            description='Для оплаты нажмите на кнопку ниже.',
#                            provider_token=provider_token,
#                            currency='rub',
#                            # photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
#                            # photo_height=512,  # !=0/None or picture won't be shown
#                            # photo_width=512,
#                            # photo_size=512,
#                            # is_flexible=True,  # True If you need to set up Shipping Fee
#                            prices=prices,
#                            start_parameter='time-machine-example',
#                            payload='HAPPY FRIDAYS COUPON')
#
#
# async def succefull_tranzzo(message):
#     print("Оплата успешно")
#     # print(message.successful_payment.total_amount / 100, message.successful_payment.currency)
#     amount = int(message.successful_payment.total_amount / 100)
#     data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#     diamond = int(amount / 10)
#     request = f"""UPDATE resource SET diamond = diamond + {diamond} WHERE user_id = {message.from_user.id};
# INSERT INTO payment(user_id, amount, data) VALUES ({message.from_user.id}, {amount}, '{data}')"""
#     print(request)
#     await sql_insertscript(request)


async def buy_qiwi(message):
    user_id = message.from_user.id
    number = (await sql_selectone(f"SELECT code FROM data"))[0]
    random_code = f"{number}{user_id}"
    markup_buy = InlineKeyboardMarkup()
    amount = int(message.text) * 10
    request = f"INSERT INTO score_payment (user_id, amount, random_code) VALUES({user_id}, {amount}, {random_code});" \
              f"UPDATE data SET code = code + 1"
    await sql_insertscript(request)
    bot_username = (await bot.me).username
    url = f"https://oplata.qiwi.com/create?publicKey={publicKeyQIWI}&amount={amount}&comment={random_code}" \
          f"&customFields[themeCode]=Konstantyn-PbboM7ch_P&successUrl=https://t.me/{bot_username}?start=check_buy"
    markup_buy.add(InlineKeyboardButton(text='Оплатить', url=url))
    # markup_buy.add(InlineKeyboardButton(text='Проверить платеж', callback_data="buy_qiwi"))
    await message.answer(text=f"Для оплаты на сумму {amount} руб. нажмите на ссылку\n", reply_markup=markup_buy)


async def buy_check_qiwi(message):
    import requests
    import json
    user_id = message.from_user.id
    api_access_token = 'c1c8cd619c5ca3eced40ca5d21e2774c'
    qiwi_account = '79233044552'
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': '50'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + qiwi_account + '/payments', params=parameters)
    req = json.loads(h.text)
    rows = await sql_select(f"SELECT amount, random_code FROM score_payment WHERE user_id = {message.chat.id}")
    for row in rows:
        for i in range(len(req['data'])):
            if req['data'][i]['comment'] == str(row[1]):
                print("коммент совпал")
                if req['data'][i]['sum']['amount'] == row[0]:
                    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    diamond = int(row[0]/10)
                    req = f"""DELETE FROM payment WHERE user_id = {message.chat.id};
                          UPDATE resource SET diamond = diamond + {diamond} WHERE user_id = {message.from_user.id};
                          INSERT INTO payment(user_id, amount, data) VALUES ({user_id}, {row[0]}, '{data}')"""
                    print(req)
                    await sql_insertscript(req)
                    text = f"Платеж на сумму %s руб. прошел\nВам начисленны %s 💎"
                    return text % (row[0], diamond)
    return "Платеж еще не прошел. Попробуйте немного позднее."
