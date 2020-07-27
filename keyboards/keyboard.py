# import telebot  # Импортируем объект бота
from aiogram.types import ReplyKeyboardMarkup
from text import texting


def keyboard_map():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_mining_map)
    return keyboard

#def keyboardmenu():
#    keyboard = ReplyKeyboardMarkup()
#    keyboard.row('🗺 Карта')
#    keyboard.row('🏘 Город')
#    return keyboard

def keyboardmap():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row (texting.button_castle)
    return keyboard

#def keyboarddel():
#    keyboard = telebot.types.ReplyKeyboardRemove()
#    return keyboard


#def keyadmin():
#    keyadmin = ReplyKeyboardMarkup()
#    keyadmin.row('Создать карту')
#    keyadmin.row("Кол-во ячеек")
#    keyadmin.row("Оплатить")
#    keyadmin.row("Новая атака")
#    return keyadmin

def keyboard_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_heroes, texting.button_building, texting.button_location)
    keyboard.row(texting.button_maps, texting.button_shop)
    keyboard.row(texting.button_setting, texting.button_help, texting.button_top)
    return keyboard
def keyboard_statisctick():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_top_castle, texting.button_top_heroes)
    keyboard.row(texting.button_back)
    return keyboard

def keyboard_map_castle():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_mining_map)
    keyboard.row(texting.button_castle)
    return keyboard

def keyboard_keyrudnic():
    keyboardmenu = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboardmenu.row(texting.button_mining)
    keyboardmenu.row(texting.button_mining_ataka)
    keyboardmenu.row (texting.button_maps)
    return keyboardmenu

def keyboard_battle():
    keyboardmenu = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboardmenu.row (texting.button_attack)
    keyboardmenu.row (texting.button_goto_two)
    return keyboardmenu

#def keyboardback():
#    keyboard = ReplyKeyboardMarkup()
#    keyboard.row('◀️Назад')
#    return keyboard


def keyboaryesno():
    keyboard = ReplyKeyboardMarkup()
    keyboard.row("Да", "Нет")
    return keyboard


def keyboard_info():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Пригласить", "💬 Чат")
    keyboard.row("Обратная связь")
    keyboard.row("Помочь проекту")
    keyboard.row (texting.button_back)
    return keyboard

def keyboard_buy():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#    keyboard.row("Tranzzo")
    keyboard.row("QIWI")
    keyboard.row (texting.button_back)
    return keyboard

def keyboard_start():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_start)
    return keyboard

def key_buy():
    keyboard = ReplyKeyboardMarkup()
    keyboard.row("Оплата QIWI")
    return keyboard

def keyboard_battle_back():
    keyboard = ReplyKeyboardMarkup()
    keyboard.row("Покинуть поле боя")
    return keyboard

def keyboard_battle_one_back():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row (texting.button_goto)
    return keyboard

def keyboard_locat():
    keyboard = ReplyKeyboardMarkup()
    keyboard.row("🗼 Осада башни")
    keyboard.row (texting.button_back)
    return keyboard

def keyboard_castle():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_castle_attack)
    keyboard.row(texting.button_castle_escape)
    return keyboard

def keyboard_castle_escape_field():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_castle_escape_field)
    return keyboard

def keyboard_buy_cancel():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texting.button_buy_cancel)
    return keyboard