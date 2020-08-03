from utils.sql import sql_selectone, sql_select
from random import randint

warrior = ['barracks', 'shooting', 'stable']


async def start_battle_tower():
    i = 0
    n = 0
    enemy_user = {}
    while i <= 5:
        i += 1
        n = 0
        request = f"SELECT SUM(barracks),SUM(shooting) ,SUM(stable) FROM siege_tower WHERE lvl = {i}"
        row = await sql_selectone(request)
        enemy_user[i] = list(row)
        request = f"SELECT user_id, barracks, shooting, stable FROM siege_tower WHERE lvl = {i}"
        rows_user = await sql_select(request)
        # for sel in row:
        #     n += 1
        #     if sel != 0:
        for row_user in rows_user:
            try:
                row_user = list(row_user)
                row_user.remove(0)
                row_user.remove(0)
                row_user.remove(0)
            except ValueError:
                pass
            print(row_user)
            qua = len(row_user)
            if qua == 1:
                pass
            else:
                s = 0
                while s < qua-1:
                    s += 1
                    print(f"s{s}")
                    r = randint(1, qua-1)
                    if r == 1:
                        await strike_calculation(enemy_user[i], warrior[r])
                        # print(war)
                        # print(warrior)
                        # war = warrior[war]

                    elif r == 2:
                        await strike_calculation(enemy_user[i], warrior[r])
                        # print(war)
                        # print(warrior)
                        # war = warrior[war]

                #     dat_old = "shooting "
                #     if self.key_old == "barracks":
                #         k = 0.5
                #     elif self.key_old == "stable":
                #         k = 1.25
                #     else:
                #         k = 1
                #     # tower_battle_boy_all( k, i, dat, dat_old)
                    elif r == 3:
                        await strike_calculation(enemy_user[i], warrior[r])
                        # print(war)
                        # print(warrior)
                        # war = warrior[war]

                #     dat_old = "stable "
                #     if self.key_old == "barracks":
                #         k = 1.25
                #     elif self.key_old == "shooting ":
                #         k = 0.5
                #     else:
                #         k = 1
                #     # tower_battle_boy_all( k, i, dat, dat_old)



async def strike_calculation(enemy_user, dat):
    r = randint(0, 2)
    if enemy_user[r] == 0:
        await strike_calculation(enemy_user, dat)
    else:
        war = warrior[r]
        if dat == "barracks" and war == "barracks" \
            or dat == "stable" and war == "stable" \
            or dat == "shooting" and war == "shooting":
            koef = 1
        elif dat == "barracks" and war == "stable" \
                or dat == "stable" and war == "shooting"\
                or dat == "shooting" and war == "barracks":
            koef = 0.5
        elif dat == "barracks" and war == "shooting" \
                or dat == "stable" and war == "barracks"\
                or dat == "shooting" and war == "stable":
            koef = 1.25
        print(f"{dat} бьет {war} koef {koef}")

    #     if self.key_old == "shooting ":
    #         k = 1.25
    #     elif self.key_old == "stable":
    #         k = 0.5
    #     else:
    #         k = 1
    #     # tower_battle_boy_all(k, i, dat, dat_old)



# def tower_comparison():
#         global tower_old, tower
#         text = ""
#         for k, v in tower_old.items():
#                     text += "Игрок " +str(k)+"\n"
#                     for key, value in tower_old[k].items():
#                         t = 1
#                         for key_old, value_old in value.items():
#                             if value_old > 0:
#
#                                 text += "Осталось " +training[key]["name"]+" "+str(key_old)+" лвл "+str(value_old)+"\n"
#                             else:
#                                 if t == 5:
#                                     text += "Все "+training[key]["name"]+" погибли\n"
#                                 t += 1
#         bot.send_message(chat_id="@HeroesLifeStat", text=text)
#
# class Battletower():
#     global tower, statistics
#     def __init__(self):
#         open_start()
#         self.key = ""
#         self.key_old = ""
#         self.tower = tower
#
#     def count_user(self):
#         if self.tower == {}:
#             print("Никто не зареган на башнюю")
#             tower_old = {}
#             save_old(tower_old)
#         else:
#             barracks = {}
#             shooting = {}
#             stable = {}
#             k = 0.2
#             logging.info('Суммируем воинов')
#
#
#             for self.key, value in self.tower.items():
#                 try:
#                     statistics[str(self.key)]["dead_one"] = 0
#                 except KeyError:
#                     statistics[str(self.key)] = {"dead_all": 0, "dead_one": 0}
#                 for self.key_old, value_old in value.items():
#                     if self.key_old == "barracks":
#                         for key_b in value_old:
#                             try:
#                                 barracks[key_b] += self.tower[self.key][self.key_old][key_b] - int(self.tower[self.key][self.key_old][key_b]*k)  # складываем значения
#                             except KeyError:  # если ключа еще нет - создаем
#                                 barracks[key_b] = self.tower[self.key][self.key_old][key_b]
#                     elif self.key_old == "shooting ":
#                         for key_b in value_old:
#                             try:
#                                 shooting[key_b] += self.tower[self.key][self.key_old][key_b] - int(self.tower[self.key][self.key_old][key_b]*k)  # складываем значения
#                             except KeyError:  # если ключа еще нет - создаем
#                                 shooting[key_b] = self.tower[self.key][self.key_old][key_b]
#                     if self.key_old == "stable":
#                         for key_b in value_old:
#                             try:
#                                 stable[key_b] += self.tower[self.key][self.key_old][key_b] - int(self.tower[self.key][self.key_old][key_b]*k)  # складываем значения
#                             except KeyError:  # если ключа еще нет - создаем
#                                 stable[key_b] = self.tower[self.key][self.key_old][key_b]
#             self.tow_all = {"barracks": barracks, "shooting ": shooting, "stable": stable}
#             logging.info(self.tow_all)
#             self.tower_all()
#             if self.tow_all == {'barracks': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0},
#                                 'shooting ': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0},
#                                 'stable': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}}:
#                 pass
#             save_old(self.tower)
#             save(self.tower)
#             save_stat()
#     def tower_all(self):
#         i = 1
#
#         while i < 5:
#             for self.key, value in self.tower.items():  # весь списо
#                 logging.info("Уровень " + str(i))
#                 logging.info("Пользователь "+ str(self.key))
#                 n = 1
#
#                 for self.key_old, value_old in value.items():  # какой то юзер
#                     logging.info("Войска "+self.key_old)
#                     for self.key_olding, self.value_olding in value[self.key_old].items():
#
#                         if self.key_olding == str(i):
#                             logging.info("Уровень воинов " + str(self.key_olding))
#                             if self.value_olding != 0:
#                                 if self.key_old == "barracks":
# #                                    print(str(self.key)+" "+self.key_old+" "+str(self.value_olding)+" "+str(i))
#                                     self.tower_battle_boy(i)
#                                 elif self.key_old == "shooting ":
# #                                    print(str(self.key)+" "+self.key_old+" "+str(self.value_olding)+" "+str(i))
#                                     self.tower_battle_boy(i)
#                                 elif self.key_old == "stable":
# #                                    print(str(self.key)+" "+self.key_old+" "+str(self.value_olding)+" "+str(i))
#                                     self.tower_battle_boy(i)
#                             else:
#                                 logging.info("Воинов уровня "+ str(self.key_olding)+ " нет")
#
#                         else:
#                             pass
#             i += 1
#   #      print(self.tower)
#   #      save()



def tower_battle_boy_all(self,  k, i, dat, dat_old):
    k = int(int(self.value_olding) * k)
    try:
        if self.tow_all[dat_old][str(i)] > 0:
            if self.tow_all[dat_old][str(i)] - k <= 0:
                print(self.tow_all[dat_old][str(i)])
                statistics[str(self.key)]["dead_all"] += self.tow_all[dat_old][str(i)]*i
                statistics[str(self.key)]["dead_one"] += self.tow_all[dat_old][str(i)]*i

                if self.tower[self.key][self.key_old][str(i)] - self.tow_all[dat_old][str(i)] <= 0:
                    self.tower[self.key][self.key_old][str(i)] = 0

                else:
                    self.tower[self.key][self.key_old][str(i)] -= self.tow_all[dat_old][str(i)]
                    self.tow_all[dat_old][str(i)] = 0
                    self.value_olding = self.tower[self.key][self.key_old][str(i)]
            else:
                print(k)
                statistics[str(self.key)]["dead_all"] += k*i
                statistics[str(self.key)]["dead_one"] += k*i
                self.tow_all[dat_old][str(i)] -= k
                self.tower[self.key][self.key_old][str(i)] = 0
        else:
            pass
    except:
        pass
