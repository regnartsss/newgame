from text.text_buy import textsell
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import LabeledPrice
from loader import bot
from data.config import provider_token
from datetime import datetime
from utils.sql import sql_insertscript
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
            await buy_tranzzo(message)


async def buy_amount(call):
    if call.data == "buy_sell":
        await call.message.answer(textsell, reply_markup=keyboard_buy_cancel())
        # await bot.send_message(chat_id=call.message.chat.id, text = textsell, reply_markup=keyboard_buy_cancel())
        await Buy.amount.set()


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


async def buy_tranzzo(message):
    amount = message.text
    prices = [LabeledPrice(label="Heroes Life", amount=int(amount) * 1000)]
    await bot.send_invoice(message.chat.id, title='Покупку алмазов в Heroes Life',
                           description='Для оплаты нажмите на кнопку ниже.',
                           provider_token=provider_token,
                           currency='rub',
                           # photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                           # photo_height=512,  # !=0/None or picture won't be shown
                           # photo_width=512,
                           # photo_size=512,
                           # is_flexible=True,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')


async def succefull_tranzzo(message):
    print("Оплата успешно")
    # print(message.successful_payment.total_amount / 100, message.successful_payment.currency)
    amount = int(message.successful_payment.total_amount / 100)
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    diamond = int(amount / 10)
    request = f"""UPDATE resource SET diamond = diamond + {diamond} WHERE user_id = {message.from_user.id};
INSERT INTO payment(user_id, amount, data) VALUES ({message.from_user.id}, {amount}, '{data}')"""
    print(request)
    await sql_insertscript(request)


"""

def buy_user(self, message):
        global users
        buy_gold = message.successful_payment.total_amount / 1000
        buy_gold = (str(buy_gold)).split(".")[0]
        users[str(self.id)]["diamond"] = users[str(self.id)]["diamond"] + int(buy_gold)
        save("all")

def payment_history_last(self, my_login, api_access_token, rows_num, next_TxnId, next_TxnDate, txnID):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + api_access_token
        parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate, 'txnID': txnID}
        h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters)
        return h.json()
"""
"""
def buy_qiwi(self):
        global amount
        pprint("asdasdasdasdasd")
        markup_buy = telebot.types.InlineKeyboardMarkup()
        markup_check = telebot.types.InlineKeyboardMarkup()
        comment = str(self.id)
        try:
            pprint(users[str(self.id)]["but_qiwi_date"])
        except:
            self.user["but_qiwi_date"] = "0"
            self.user["but_qiwi_date_down"] = "0"
        try:
            pprint(self.user["buy_qiwi_check"])
        except:
            self.user["buy_qiwi_check"] = 1
        pprint(self.user["buy_qiwi_check"])
        pprint(users[str(self.id)]["but_qiwi_date"])

        if self.user["buy_qiwi_check"] == 0 and date("utctime") < users[str(self.id)]["but_qiwi_date"]:
            markup_check.add(telebot.types.InlineKeyboardButton(text='Проверить платеж', callback_data="buy_qiwi"))
            text = "Проверить платеж"
            bot.send_message(self.id, text, reply_markup=markup_check)

        elif self.user["but_qiwi_date_down"] > date("utctime"):
            bot.send_message(self.id,
                             text="Вы уже создали счет на оплату, оплатите его или повторите попытку через час")
            markup_check.add(telebot.types.InlineKeyboardButton(text='Проверить платеж', callback_data="buy_qiwi"))
            text = "Проверить платеж"
            bot.send_message(self.id, text, reply_markup=markup_check)
        else:
            pprint("bnbnbnnb")
            markup_buy.add(telebot.types.InlineKeyboardButton(text='Оплатить',
                                                              url="https://oplata.qiwi.com/create?publicKey=" 
                                                              + publicKey +
                                                                  "&amount=" + str(
                                                                  int(
                                                                      self.text) * 1) + "&comment=" + comment 
                                                                      + "&customFields[themeCode]=
            Konstantyn-PbboM7ch_P&successUrl=https%3A%2F%2Ft.me%2FHeroesLifeBot&lifetime=" + date(
                                                                  'buyqiwi')))
            self.user["buy_qiwi_tranzaction"] = 0
            self.user["buy_qiwi_comment"] = comment
            self.user["buy_qiwi_amount"] = int(self.text)
            self.user["but_qiwi_date_down"] = date('buytimedown')
            self.user["but_qiwi_date_up"] = date('buytimeup')
            self.user["buy_qiwi_check"] = 0
            pprint("asdasd")
            text = "Для покупки " + str(int(self.text)) + " 💎 нажмите на кнопку ниже \nПокупка на сумму " + str(
                int(self.text) * 10) + " руб."
            pprint("zxczxc")
            bot.send_message(self.id, text, reply_markup=markup_buy)
            markup_check.add(telebot.types.InlineKeyboardButton(text='Проверить платеж', callback_data="buy_qiwi"))
            text = "Проверить платеж"
            bot.send_message(self.id, text, reply_markup=markup_check)
        save("users")

def buy_check_qiwi(self):
        api_access_token = '9f5335d8b6e7d3bfdc336db48a160a17'
        mylogin = '79233044552'

        comment = str(self.id)
        lastPayments = self.payment_history_last(mylogin, api_access_token, '3', '', '', comment)
        #        pprint(lastPayments)
        #        pprint(lastPayments)

        for i in range(len(lastPayments['data'])):
            comment = lastPayments['data'][i]['comment']
            status = lastPayments['data'][i]['status']
            txnId = lastPayments['data'][i]['txnId']
            amount = lastPayments['data'][i]['sum']['amount']
            date = lastPayments['data'][i]['date']

            if comment == str(self.id) and status == 'SUCCESS':
                if users[str(self.id)]["but_qiwi_date_down"] < date < users[str(self.id)]["but_qiwi_date_up"]:
                    if self.user["buy_qiwi_check"] == 0:
                        pprint("Платеж прошел успешно")
                        bot.send_message(self.id, "Счет " + str(txnId) + " на сумму " + str(
                            amount) + " руб " + date + ". Оплачен",
                                         reply_markup=keyboard_info())
                        users[str(self.id)]["but_qiwi_date"] = "0"
                        self.user["buy_qiwi_check"] = 1
                        buy_gold = int(amount)
                        users[str(self.id)]["diamond"] = users[str(self.id)]["diamond"] + buy_gold
                    else:
                        bot.send_message(self.id, "Начисление уже было произведено")
                        break
            #       else:
            #            bot.send_message(self.id, "Счет не был оплачен во время")
            else:
                bot.send_message(self.id, "Счет на сумму " + str(amount) + " руб " + date + ". Не оплачен",
                                 reply_markup=keyboard_main_menu())

        #                pprint("Чужой счет " + str(txnId) + " на сумму " + str(amount) + " руб. Оплачен")
        #            pprint(lastPayments['data'][i]['txnId'])
        #            pprint(lastPayments['data'][i]['comment'])
        #            pprint(lastPayments['data'][i]['sum']['amount'])
        #            pprint(lastPayments['data'][i]['date'])

        st = lastPayments['data'][0]['status']
        txnId = lastPayments['data'][0]['txnId']
        s = lastPayments['data'][0]['sum']['amount']
        commentId = lastPayments['data'][0]['comment']
        comment = users[str(self.id)]["buy_qiwi_comment"]
        save("all")


        if users[str(self.id)]["buy_qiwi_tranzaction"] == txnId:
            bot.send_message(self.id, 'Нет выставленных счетов на оплату')

        elif st == 'SUCCESS' and comment == commentId:
            bot.send_message(self.id, 'Ура! Спасибо за оплату! Заказ на сумму '+str(s)+' руб.')
            buy_gold = int(s)
            users[str(self.id)]["gold"] = users[str(self.id)]["gold"] + buy_gold
            users[str(self.id)]["buy_qiwi_tranzaction"] = txnId
            save("all")

        else:
            bot.send_message(self.id, "Платеж не прошел, оплатите счет")

        pprint(st)
    """