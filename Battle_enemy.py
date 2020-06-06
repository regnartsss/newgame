from pprint import pprint
import random
import json
import os
from collections import Counter
from aiogram import types
from misc import dp, bot

# import numpy as np
# from numpy.random import randint as rand

# def field_new(message):
#     lvl = int(message.text)
#     k = [4, 2.5, 2, 1.75, 1.6]
# #    keyboard = []
# #    keyboard = telebot.types.InlineKeyboardMarkup()
#     f = []
#     k_k = int(k[lvl - 1] * lvl)
#     x = 1
#     s = 5
#     r = random.randint(1, k_k)
#     t, n, k = 0, 1, 3
#     t_t, n_n = 4, 2
#     h = -1
# #    tab = []
#     while x <= k_k:
#         y = 1
#         tab = []
#         while y <= k_k:
#             if y == r and x == 1:
#                 tab.append(2)
#                 r = y
#             elif y == 1:
#                 if y == r:
#                     r = random.randint(2, s)
#                     if r == 2:
#                         r = y
#                         tab.append(0)
#                         s = 5
#                     elif r == 3 or r == 4 or r == 5:
#                         r = y + 1
#                         tab.append(0)
#                         t = 2
#                         t_t = 5
#                 else:
#                     tab.append(1)
#             elif y == k_k:
#                 if y == r:
#                     r = random.randint(h, 2)
#                     print("право %s" %r)
#                     if r == 1 or r == 0 or r == -1:
#                         tab, r, t, t_t,h = left(tab, y, t, t_t,h)
#                         # tab.insert(y-1, 0)
#                         # tab.insert(y, 0)
#                         # try:
#                         #     tab.pop(1)
#                         # except:
#                         #     print("error_1")
#                         # r = y - 1
#                         # t = - 1
#                         # t_t = 2
#                     elif r == 2:
#                         r = y
#                         tab.append(0)
#                         h =- 1
#                 else:
#                     tab.append(1)
#             else:
#                 if y == r:
#                     r = random.randint(t, t_t)
#                     print("Середина %s" % r)
#                     if r == 1 or r == 0 or r == -1:
#                         tab, r, t, t_t,h = left(tab, y, t, t_t,h)
#                         print("Выход %s" %tab)
#                         # tab.insert(y-1, 0)
#                         # tab.insert(y, 0)
#                         # try:
#                         #     tab.pop(1)
#                         # except:
#                         #     print("error_1")
#                         # r = y-1
#                         # t = - 1
#                         # t_t = 2
#                         s = 2
#                     elif r == 2:
#                         r = y
#                         tab.append(0)
#                         t = -1
#                         t_t = 5
#                     elif r == 4 or r == 3 or r == 5:
#                         r = y + 1
#                         tab.append(0)
#                         t = 2
#                         t_t = 5
#                         h = 2
#                 else:
#                     tab.append(1)
#             y += 1
#         f.append(tab)
#         x += 1
#     pprint(f)
#     field[str(message.chat.id)] = f
#     save()
#     field_enemt()
# #    bot.send_message(text="Battle", chat_id=765333440)
#
# def field_enemt():
#     i=0
#     num = []
#     for k,v in field.items():
#         while i < len(v):
#             num.extend(field[k][i])
#             i += 1
#     print(num)
#     c = num.count(0)
#     print(c)
#
# #bot.send_message(text="Battle", chat_id=765333440)
# #open_o()
#
# def left(tab,y,t,t_t,h):
#     r = random.randint(t, t_t)
#     print("Выпало " + str(r))
#     if r == 1 or r == 0 or r == -1:
#         tab.insert(y - 1, 0)
# #        tab.insert(y, 0)
#         try:
#             tab.pop(1)
#         except:
#             print("error_1")
#         r = y - 1
#         t = - 1
#         t_t = 2
#         left(tab, y, t, t_t,h)
#         return tab, r, t, t_t,h
#     elif r == 2:
#         r = y
#         tab.append(0)
#         t = -1
#         t_t = 5
#         return tab, r, t, t_t, h
#     elif r == 4 or r == 3 or r == 5:
#         r = y + 1
#         tab.append(0)
#         t = 2
#         t_t = 5
#         h = 2
#         return tab, r, t, t_t, h
#     else:
#         print(tab)
#         return tab, r, t, t_t
#
# def s():
#     tab = [1, 1, 1, 1, 1, 1, 1, 1, 0]
#     y = 9
#     k = -1
#     k_k = 3
#     tab = left(tab, y, k, k_k)
#     print("итог " + str(tab))
#
# #s()
#

def r_print_r(self, st=""):
    keyboard = types.InlineKeyboardMarkup()
    a = field[str(self.message_chat_id)]
    dd = {0: " ", 1: "🌲", 2: "🕴", 3: "👻"}
    l = len(a)
    k_k = l ** 0.5
    f = []
    x, y, n = 1, 1, 0

    while x <= k_k:
        tab = []
        keyfield = []
        y = 1
        while y <= k_k:
                tab.append(a[n])
#                    print("error_2")
                keyfield.append(types.InlineKeyboardButton(text="%s" % dd[a[n]], callback_data="field_%s_%s" % (a[n], n)))
                y += 1
                n += 1
        x += 1
        f.append(tab)
        keyboard.row(*keyfield)
#        pprint(f)
    if st == "new":
      bot.send_message(text="Ходите", chat_id=self.message_chat_id,reply_markup=keyboard)
    else:
        try:

            bot.edit_message_text(text="Ходите", chat_id=self.message_chat_id, message_id=self.call_message_id, reply_markup=keyboard)
        except: pass


def field_goto(self):
    if self.message_text == "111":
        self.r_print_r("new")
    else:
        print(self.call.data)
        i = 0
        print("her_1")
        while i <= len(self.field):
#                print(self.field[i])
            if self.field[i] == 2:
                her = i
                break
            i +=1
        cell = int(self.call.data.split("_")[2])
        result = int(self.call.data.split("_")[1])
        print(result)
        print("Игрок %s ходит на %s" %(her, cell))
        if result == 1:
            print("dddd")
            try:
                await bot.answer_callback_query(callback_query_id=self.call_id, text="Ячейка не доступна")
            except:
                pass
        elif result == 0 or result == 3:
            print("num_2")
#                print(self.field)
            if her - cell == 1 or cell - her == 1 or cell - her == 5 or her - cell == 5:
                print("rez %s" %result)
                if result == 3:
                    print(result)
                    print("атака")
                else:
                    self.field[her] = 0
                    self.field[cell] = 2
                    r_print_r()

            else:
                print("Ошибка")

def r__r():
    keyboard = types.InlineKeyboardMarkup()
    a = field[str(self.message_chat_id)]
    dd = {0: " ", 1: "🌲", 2: "🕴", 3: "👻"}
    l = len(a)
    k_k = l ** 0.5
    if k_k == 8:
        lvl = 5
    elif k_k == 7:
        lvl = 4
    elif k_k == 6:
        lvl = 3
    elif k_k == 5:
        lvl = 2
    elif k_k == 4:
        lvl = 1
    #    x, y, n = 1, 1, 0
    r = int(a.count(0) / lvl - 1)
    f = []
    x, y, n = 1, 1, 0
    r_r = r
    s = 0
    print(33333)

    while x <= k_k:
        tab = []
        keyfield = []
        y = 1
        while y <= k_k:
            print("error_1")
            if a[n] == 0:
                if s == r_r:
                    print("error_2")
                    a[n] = 3
                    tab.append(a[n])
                    print("error_2")
                    keyfield.append(types.InlineKeyboardButton(text="%s" % dd[a[n]],
                                                                       callback_data="field_%s_%s" % (a[n], n)))
                    r_r += r
                else:
                    print("error_3")
                    tab.append(a[n])
                    print("error_2")
                    keyfield.append(types.InlineKeyboardButton(text="%s" % dd[a[n]],
                                                                       callback_data="field_%s_%s" % (a[n], n)))
                s += 1
                y += 1
                n += 1
            else:
                print("error_4")
                print(dd[a[n]])
                print("error_4")
                tab.append(a[n])
                print("error_4")
                keyfield.append(
                    types.InlineKeyboardButton(text="%s" % dd[a[n]], callback_data="field_%s_%s" % (a[n], n)))
                print("error_4")
                y += 1
                n += 1
        x += 1
        f.append(tab)
        keyboard.row(*keyfield)
    pprint(f)
    print(s)
    bot.send_message(text="Ходите}", chat_id=self.message_chat_id, reply_markup=keyboard)

#
# # bot.send_message(text="🏘 Домой", chat_id=765333440)
#
# @bot.message_handler(content_types=['text'])
# def send_text(message):
# if message.text == "111":
#     Field_enemy(message).field_goto()
# else:
#     print(message.text)
# #      field_new(message=message)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
# if call.data.split("_")[0] == "field":
#     Field_enemy(message=call.message, call=call).field_goto()
#
# #bot.infinity_polling(True)
# bot.polling()

#
# def s():
#     tab = [1, 1, 1, 1, 1, 1, 1, 1, 0]
#     y = 9
#     r = random.randint(-1, 3)
#     print(r)
#     if r == 1 or r == 0 or r == -1:
#         tab.insert(y - 1, 0)
#         tab.append(0)
#         try:
#             tab.pop(1)
#         except:
#             print("error_1")
#         r = y - 1
#         t = - 1
#         t_t = 2
#     print(tab)
#
# s()
