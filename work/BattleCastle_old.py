import random
from utils.sql import sql_select


def castle_start(one, two):
    lvl_castle_one, lvl_castle_two = 0, 0
    request = f"SELECT user_id, castle FROM heroes WHERE user_id = {one} or user_id = {two}"
    print(request)
    rows = await sql_select(request)
    print(rows)
    for row in rows:
        if row[0] == one:
            lvl_castle_one = row[1]
        elif row[0] == two:
            lvl_castle_two = row[1]

    if lvl_castle_one >= lvl_castle_two:
        lvl_castle = await castle_start_lvl(lvl_castle_two)
        print(lvl_castle)
        return await castle_start_queue(one, two, lvl_castle)
    elif lvl_castle_one <= lvl_castle_two:
        lvl_castle = await castle_start_lvl(lvl_castle_one)
        print(lvl_castle)
        return await castle_start_queue(one, two, lvl_castle)


async def castle_start_lvl(lvl_castle):
    if 0 < lvl_castle <= 4:
        return 1
    elif 4 < lvl_castle <= 8:
        return 2
    elif 8 < lvl_castle <= 12:
        return 3
    elif 12 < lvl_castle <= 16:
        return 4
    elif 16 < lvl_castle <= 20:
        return 5


async def castle_start_queue(one, two, lvl_war, warrior):
    print("castle_start_queue_1")
    stat_one = (sorted(warrior[str(one)].items(), key=lambda k: k[1][str(lvl_war)]))
    stat_two = (sorted(warrior[str(two)].items(), key=lambda k: k[1][str(lvl_war)]))
    queue = {"q": [], "q_one": [], "q_two": []}
    for key, value in stat_one:
        if value[str(lvl_war)] == 0:
            pass
        else:
            queue["q_one"].append(key)

    for key, value in stat_two:
        if value[str(lvl_war)] == 0:
            pass
        else:
            queue["q_two"].append(key)
    #    print(queue["q_one"])
    if queue["q_one"] == []:
        print("У вас нет воинов %s уровня" % lvl_war)
        return "У вас нет воинов %s уровня" % lvl_war
    if queue["q_two"] == []:
        print("У соперника нет воинов %s уровня" % lvl_war)
        return "У соперника нет воинов %s уровня" % lvl_war

    i = 0
    while i < 3:
        try:
            queue["q"].append("%s_one" % queue["q_one"][i])
        except:
            pass

        try:
            queue["q"].append("%s_two" % queue["q_two"][i])
        except:
            pass
        i += 1
    queue.pop("q_one")
    queue.pop("q_two")
    castle = {"user_one": one, "user_two": two, "lvl_war": str(lvl_war), "start_one": 0, "start_two": 0,
              "chat_id_one": 0, "chat_id_two": 0, "dead_one":0, "dead_two":0,
              "goto": " ", "que": 0, "q": queue["q"], "field": [], "t_one": [0, 16, 32, 48], "t_two": [63, 47, 31, 15]}
    castle = {"user_one": one, "user_two": two, "lvl_war": str(lvl_war), "start_one": 0, "start_two": 0,
              "chat_id_one": 0, "chat_id_two": 0, "dead_one":0, "dead_two":0,
              "goto": " ", "que": 0, "q": queue["q"], "field": [], "t_one": [19,35], "t_two": [20,36]}
    print(castle)
    return castle


def castle_keyboard_start(castle):
    keyboard_one = telebot.types.InlineKeyboardMarkup()
    keyboard_two = telebot.types.InlineKeyboardMarkup()
    keyboard_one.row(telebot.types.InlineKeyboardButton("Автоматически",
                                                        callback_data="castle_auto_%s" % castle["user_one"]))
    keyboard_one.row(telebot.types.InlineKeyboardButton("Вручную",
                                                        callback_data="castle_manual_%s" % castle["user_one"]))
    keyboard_two.row(telebot.types.InlineKeyboardButton("Автоматически",
                                                        callback_data="castle_auto_%s" % castle["user_two"]))
    keyboard_two.row(telebot.types.InlineKeyboardButton("Вручную",
                                                        callback_data="castle_manual_%s" % castle["user_two"]))
    return keyboard_one, keyboard_two


def castle_place_troops(key):
    key["field"] = [0 for i in range(0, 64)]
    key["goto"] = key["q"][0]
    i = 0
    while i < len(key["field"]):
        if key["field_one"][i] != 0:
            key["field"][i] = key["field_one"][i]
        elif key["field_two"][i] != 0:
            key["field"][i] = key["field_two"][i]
        i += 1
    # key["q"].append("user_one")
    # key["q"].append("user_two")
    for t in key["q"]:
        if t == "user_one":
            castle_place_troops_random("t_one", key, t)
        elif t == "user_two":
            castle_place_troops_random("t_two", key, t)
        elif t == "barracks_one":
            castle_place_troops_random("t_one", key, t)
        elif t == "barracks_two":
            castle_place_troops_random("t_two", key, t)
        elif t == "shooting_one":
            castle_place_troops_random("t_one", key, t)
        elif t == "shooting_two":
            castle_place_troops_random("t_two", key, t)
        elif t == "stable_one":
            castle_place_troops_random("t_one", key, t)
        elif t == "stable_two":
            castle_place_troops_random("t_two", key, t)
        # elif t == "tower":
        #     key["field"][56] = t


def castle_place_troops_random(user, key, t):
    r = random.choice(key[user])
    key["field"][r] = t
    key[user].remove(r)


def castle_keyboard_castle(key, move_2, warrior):
    print("keyboard_castle")
    castle_battle(key)
    keyboard_one = telebot.types.InlineKeyboardMarkup()
    keyboard_two = telebot.types.InlineKeyboardMarkup()
    x, y, n, s = 0, 0, 0, 8
    one = ["user_one", "barracks_one", "shooting_one", "stable_one"]
    two = ["user_two", "barracks_two", "shooting_two", "stable_two"]
    while x < s:
        tab_one = []
        tab_two = []
        y = 0
        while y < s:
            if key["field"][n] == "user_one":
                tab_one.append(telebot.types.InlineKeyboardButton("🚶‍♂", callback_data="hit_user_one"))
                tab_two.append(telebot.types.InlineKeyboardButton("🚶‍♂", callback_data="hit_user_one"))

            elif key["field"][n] == "user_two":
                tab_one.append(telebot.types.InlineKeyboardButton("🚶‍♂", callback_data="hit_user_two"))
                tab_two.append(telebot.types.InlineKeyboardButton("🚶‍♂", callback_data="hit_user_two"))

            elif key["field"][n] == "barracks_one":
                tab_one.append(telebot.types.InlineKeyboardButton("⚔", callback_data="hit_barracks_one"))
                tab_two.append(telebot.types.InlineKeyboardButton("⚔", callback_data="hit_barracks_one"))

            elif key["field"][n] == "barracks_two":
                tab_one.append(telebot.types.InlineKeyboardButton("⚔", callback_data="hit_barracks_two"))
                tab_two.append(telebot.types.InlineKeyboardButton("⚔", callback_data="hit_barracks_two"))

            elif key["field"][n] == "shooting_one":
                tab_one.append(telebot.types.InlineKeyboardButton("🏹", callback_data="hit_shooting_one"))
                tab_two.append(telebot.types.InlineKeyboardButton("🏹", callback_data="hit_shooting_one"))

            elif key["field"][n] == "shooting_two":
                tab_one.append(telebot.types.InlineKeyboardButton("🏹", callback_data="hit_shooting_two"))
                tab_two.append(telebot.types.InlineKeyboardButton("🏹", callback_data="hit_shooting_two"))

            elif key["field"][n] == "stable_one":
                tab_one.append(telebot.types.InlineKeyboardButton("🐴", callback_data="hit_stable_one"))
                tab_two.append(telebot.types.InlineKeyboardButton("🐴", callback_data="hit_stable_one"))
            elif key["field"][n] == "stable_two":
                tab_one.append(telebot.types.InlineKeyboardButton("🐴", callback_data="hit_stable_two"))
                tab_two.append(telebot.types.InlineKeyboardButton("🐴", callback_data="hit_stable_two"))

            elif key["field"][n] == 1 and move_2 in one:
                tab_one.append(telebot.types.InlineKeyboardButton("✳", callback_data="step_%s" % n))
                tab_two.append(telebot.types.InlineKeyboardButton(" ", callback_data="l_%s" % n))
            elif key["field"][n] == 1 and move_2 in two:
                tab_one.append(telebot.types.InlineKeyboardButton(" ", callback_data="l_%s" % n))
                tab_two.append(telebot.types.InlineKeyboardButton("✳", callback_data="step_%s" % n))
            elif key["field"][n] == "tower":
                tab_one.append(telebot.types.InlineKeyboardButton("⛩", callback_data="step_tower"))
                tab_two.append(telebot.types.InlineKeyboardButton("⛩", callback_data="l_%s"))

            # elif key["field"][n] == 3 and str(call.message.chat.id) == str(key["user_one"]):
            #     tab_one.append(telebot.types.InlineKeyboardButton(" ", callback_data="start_null"))
            #     tab_two.append(telebot.types.InlineKeyboardButton("🗡", callback_data="start_null"))
            #
            # elif key["field"][n] == 3 and str(call.message.chat.id) == str(key["user_two"]):
            #     tab_one.append(telebot.types.InlineKeyboardButton("🗡", callback_data="start_null"))
            #     tab_two.append(telebot.types.InlineKeyboardButton(" ", callback_data="start_null"))

            else:
                tab_one.append(telebot.types.InlineKeyboardButton(" ", callback_data="start_null"))
                tab_two.append(telebot.types.InlineKeyboardButton(" ", callback_data="start_null"))
            y += 1
            n += 1
        keyboard_one.row(*tab_one)
        keyboard_two.row(*tab_two)
        x += 1

    text_one, text_two = text_total_war(key, warrior)
    keyboard_one.row(telebot.types.InlineKeyboardButton(text_one, callback_data="step_null"))
    keyboard_two.row(telebot.types.InlineKeyboardButton(text_two, callback_data="step_null"))
    if move_2 in one:
        keyboard_one.row(telebot.types.InlineKeyboardButton("Пропустить ход", callback_data="step_break"))
        keyboard_two.row(telebot.types.InlineKeyboardButton("Ход соперника", callback_data="step_break"))
    elif move_2 in two:
        keyboard_two.row(telebot.types.InlineKeyboardButton("Пропустить ход", callback_data="step_break"))
        keyboard_one.row(telebot.types.InlineKeyboardButton("Ход соперника", callback_data="step_break"))
    print("Поле готово")
    return keyboard_one, keyboard_two


def text_total_war(key, warrior):
    print("text_total_war")
    lvl_war = str(key["lvl_war"])
    user_one = str(key["user_one"])
    user_two = str(key["user_two"])
    text_one = "⚔: %s️🏹: %s 🐴: %s" % \
               (warrior[user_one]["barracks"][lvl_war], warrior[user_one]["shooting"][lvl_war],
                warrior[user_one]["stable"][lvl_war])
    text_two = "⚔: %s️🏹: %s 🐴: %s" % \
               (warrior[user_two]["barracks"][lvl_war], warrior[user_two]["shooting"][lvl_war],
                warrior[user_two]["stable"][lvl_war])
    return text_one, text_two


def castle_battle(key):
    print("castle_battle")
    # for ss in key["field"]:
    #     if ss == key["goto"]:
    if key["goto"] == "user_one":
        castle_calculation(key, "user_one")
    elif key["goto"] == "user_two":
        castle_calculation(key, "user_two")
    elif key["goto"] == "barracks_one":
        castle_calculation(key, "barracks_one")
    elif key["goto"] == "barracks_two":
        castle_calculation(key, "barracks_two")
    elif key["goto"] == "shooting_one":
        castle_calculation(key, "shooting_one")
    elif key["goto"] == "shooting_two":
        castle_calculation(key, "shooting_two")
    elif key["goto"] == "stable_one":
        castle_calculation(key, "stable_one")
    elif key["goto"] == "stable_two":
        castle_calculation(key, "stable_two")
    # elif key["goto"] == "tower":
    #     castle_calculation(key, "tower")


def castle_calculation(key, data):
    print("calculation_1")
    print(data)
    print(key["field"])
    nn = key["field"].index(data)
    print(nn)
    move = data.split("_")[0]
    user = data.split("_")[1]
    if move == "user":
        pole = [-8, -1, 0, 1, 8]
        castle_cal_pole(key, pole, nn, 1)
    if move == "barracks":
        pole = [-9, -7, -8, -1, 0, 1, 8, 7, 9]
        castle_cal_pole(key, pole, nn, 1)
    if move == "stable":
        pole = [-16, -2, -8, -1,0, 1, 8, 2, 16]
        castle_cal_pole(key, pole, nn, 1)
    if move == "shooting":
        pole = [-8, -1,0, 1, 8]
        castle_cal_pole(key, pole, nn, 1)

    # if data == "tower":
    #     pole = [-8, -1, 1, 8]
    #     cal_pole_one(key, pole, nn, 3)


def castle_cal_pole(key, pole, nn, kof):
    print("cal_pole")
    cell_null = [0, 1, 8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57]
    cell_old = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55, 62, 63]
    for g in pole:
        if nn in cell_null:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0 and nn + g not in cell_old:
                    key["field"][nn + g] = kof

        if nn in cell_old:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0 and nn + g not in cell_null:
                    key["field"][nn + g] = kof

        if nn not in cell_null and nn not in cell_old:
            if 0 <= nn + g <= 63:
                if key["field"][nn + g] == 0:
                    key["field"][nn + g] = kof


# def text_message(key, move_1):
#     print("text_message")
#     text_1, text_2 = "null", "null"
#     if move_1 == "user_one":
#         text_2 = "Ходите героем"
#         text_1 = "Ожидайте хода соперника"
#     elif move_1 == "barracks_one":
#         text_2 = "Ходите воинами"
#         text_1 = "Ожидайте хода соперника"
#     elif move_1 == "shooting_one":
#         text_2 = "Ходите лучниками"
#         text_1 = "Ожидайте хода соперника"
#     elif move_1 == "stable_one":
#         text_2 = "Ходите всадниками"
#         text_1 = "Ожидайте хода соперника"
#     elif move_1 == "user_two":
#         text_1 = "Ходите воинами"
#         text_2 = "Ожидайте хода соперника"
#     elif move_1 == "barracks_two":
#         text_1 = "Ходите лучниками"
#         text_2 = "Ожидайте хода соперника"
#     elif move_1 == "shooting_two":
#         text_1 = "Ходите всадниками"
#         text_2 = "Ожидайте хода соперника"
#     elif move_1 == "stable_two":
#         text_1 = "Ходите героем"
#         text_2 = "Ожидайте хода соперника"
#     return text_1, text_2


def castle_hit(key, move_1, hit, warrior):
    print("castle_hit_1")
    print("%s %s" % (move_1, hit))
    move = move_1.split("_")[0]
    hit_one = key["field"].index(move_1)
    hit_two = key["field"].index(hit)
    hit_old = hit_one - hit_two
    pole = []
    if move == "user":
         pole = [-8, -1, 1, 8]
         # cal_pole_one(key, pole, nn, 1)
    if move == "barracks":
         pole = [-9, -7, -8, -1, 1, 8, 7, 9]
         # cal_pole_one(key, pole, nn, 1)
    if move == "stable":
         pole = [-16, -2, -8, -1, 1, 8, 2, 16]
         # cal_pole_one(key, pole, nn, 1)
    if move == "shooting":
         pole = [-8, -1, 1, 8]
         # cal_pole_one(key, pole, nn, 1)

    if hit_old in pole:
        print("Удар от %s по %s" % (move_1, hit))
        war_one = move_1.split("_")[0]
        war_two = hit.split("_")[0]
        print("castle_hit")
        print(war_one)
        print(war_two)
    # Воины - Лучники
        if war_one == "barracks" and war_two == "shooting":
            koef = 1.25
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
    # Воины - Всадники
        elif war_one == "barracks" and war_two == "stable":
            koef = 0.75
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
    # Лучники - Воины
        elif war_one == "shooting" and war_two == "barracks":
            koef = 0.75
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
    # Лучники - Всадники
        elif war_one == "shooting" and war_two == "stable":
            koef = 1.25
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
    # Всадники - Воины
        elif war_one == "stable" and war_two == "barracks":
            koef = 1.25
            n= calculation_hit(key, koef, warrior, move_1, hit)
            return n
    # Всадники - Лучники
        elif war_one == "stable" and war_two == "shooting":
            koef = 0.75
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
        else:
            koef = 1
            n = calculation_hit(key, koef, warrior, move_1, hit)
            return n
        # key["q"].remove(hit)
        # # key["field"][hit_one] = 0
        # # key["field"][hit_two] = move_1
        # return hit_two
    else:
        return  False
def calculation_hit(key, koef, warrior, move_1, hit):
    hit_one = key["field"].index(move_1)
    hit_two = key["field"].index(hit)
    war_one = move_1.split("_")[0]
    war_two = hit.split("_")[0]
    lvl_war = str(key["lvl_war"])
    user_one = str(key["user_one"])
    user_two = str(key["user_two"])
    print(war_one)
    print(war_two)
    print(warrior[user_one])
    print(warrior[user_two])
    print(warrior[user_one][war_one][lvl_war])
    print(warrior[user_two][war_two][lvl_war])
    num_one = int(warrior[user_one][war_one][lvl_war])
    num_two = int(warrior[user_two][war_two][lvl_war])
    print(war_one)
    print(lvl_war)
    attack_one = training[war_one][int(lvl_war)]["attack"]
    attack_two = training[war_two][int(lvl_war)]["attack"]
    defence_one = training[war_one][int(lvl_war)]["defence"]
    defence_two = training[war_two][int(lvl_war)]["defence"]
    health_one = training[war_one][int(lvl_war)]["health"]
    health_two = training[war_two][int(lvl_war)]["health"]
    stat_one = num_one * attack_one * health_one * koef
    stat_two = num_two * defence_two * health_two
    total = stat_one - stat_two

    if total == 0:
        warrior[user_one][war_one][lvl_war] = 0
        warrior[user_two][war_two][lvl_war] = 0
        key["field"][hit_two] = 0
        key["field"][hit_one] = 0
        key["q"].remove(move_1)
        key["q"].remove(hit)
    elif total < 0:
        print("Убил не всех")
        print(total / defence_two / health_two)
        warrior[user_one][war_one][lvl_war] = 0
        warrior[user_two][war_two][lvl_war] = int(total / defence_two / health_two)* -1
        key["q"].remove(move_1)
        # move_2 = key["q"][key["que"]]
        # n = int(key["field"].index(move_2))
        # return n
        key["field"][hit_one] = 0
        # # key["field"][hit_one] = move_1
        key["dead_one"] += num_two + int(total / defence_two / health_two)
        key["dead_two"] += num_one
    else:
        print("Убил всех")
        print(total / attack_one / health_one)
        warrior[user_two][war_two][lvl_war] = 0
        warrior[user_one][war_one][lvl_war] -= int(total / attack_one / health_one)
        # if warrior[user_one][war_one][lvl_war] < 0:
        #     warrior[user_one][war_one][lvl_war] = 0
        key["q"].remove(hit)
        # key["field"][hit_one] = 0
        key["field"][hit_two] = 0
        key["dead_one"] += num_one
        key["dead_two"] += int(total / attack_one / health_one)
        # return hit_two



    #     # pole = [-32, -24, -16, -8, -23, -15, -7, -14, -6, -5, 1, 2, 3, 4, 8, 9, 10, 11, 16, 17, 18, 24, 25, 32]
    #     # cal_pole_one(key, pole, nn, 3)
    # print(hit_one)
    # print(hit_two)
    # # print(pole)
    # data = hit_one - hit_two
    # if data in pole:
    #     print("Удар от %s по %s" % (move_1, hit))
    #     print(key["q"])
    #     # key["q"].remove(hit)
    #     # print(key["q"])
    #
    # else:
    #     print("Промах")

#     # if data == "tower":
#     #     pole = [-8, -1, 1, 8]
#     #     cal_pole_one(key, pole, nn, 3)
# #
