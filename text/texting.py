from utils import sql

#
# def benchmark(func):
#     global st
#
#     def wrapper(*args, **kwargs):
#         t = time.time()
#         res = func(*args, **kwargs)
#         print(func.__name__, time.time() - t)
#         return res
#
#     return wrapper


button_heroes = "🤴🏻 Герой"
button_building = "⚒ Строения"
button_location = "🏞 Локации"
button_shop = "💎 Магазин"
button_help = "❓ Помощь"
button_top = "🏆 Рейтинг"

button_castle = "🏰 Вернуться в замок"
button_setting = "⚙ Настройки"
button_back = "⬅ Назад"
button_attack = "⚔ Атаковать"

button_buy_cancel = "🚫 Отмена"

button_mining = "⛏ Добыча"
button_mining_ataka = "⚔ Пройти?"

button_start = "Начать игру"
button_update = "⚒ Улучшить"
button_market = "🎪 Рынок"
button_top_heroes = "🥇 Топ по уровню"
button_top_castle = "🏰 Топ по замку"
button_castle_attack = "⚔ Напасть на замок"

text_setting = "⚙ Настройки"
text_goto_maps = "🚶‍♂ Делайте ход по игровому полю"
text_goto = "🚶‍♂ Ходите"
text_user_is = "Пользователь есть"
text_user_new = " Зарегистрирован новый пользователь "
text_user_name = "Введите имя своего 🤴🏻 героя или используйте предложенное, нажав на кнопочку"
text_building_update = "Здесь вы можете улучшить ваши постройки\n %s"
text_mining_start = "Вы начали добычу ресурса.\n Это может занять некоторое время ⏱.\n После окончания добычи, Вам придет уведомление ⏰. \n Для ОТМЕНЫ, нажмите Вернуться на карту 🗺"
text_mining_ataka = "Пройдите вручную"
text_energy_timer = "Энергия полностью восстановлена"
text_building_up = "💥 Здание улучшено\n"
text_building_goto = "Войти в здание"
text_start = "Добро пожаловать в фантазийную игру. Управляя героем, находи клады и выполняй миссии," \
             " чтобы заработать денег. Увеличивай свою армию. Пошаговое ведение боя.\n " \
             "Движение по карте осуществляется с помощью кнопочек ➡️⬇️⬆️⬅️. " \
             "На карте распологаются различные ресурсы: ⛏камень, 🌲дерево, 🔨 еда и монстры, " \
             "которых вы можете атаковать"
text_main_menu = "Добро пожаловать %s. Начните свою игру с освоения карты и добычы необходимых для ресурсов, " \
                 "для постройки зданий"
text_mail = "Игра была обновлена, внесены следующие изменения:\n⚔ Атака монстров на карте\n" \
            "⚒ Строительство зданий в замке\n🏹 Обучение воинов\nДля обновления нажмите /button\n" \
            "По вопросам и предложениям пишите @HeroesLi "
text_ataka_enemy = "Вы напали на %s - 🏅%s  ❤%s \n" \
                   "Что будете делать? 🔋1\n ⚔️Атаковать или 🏃‍♂️Отступить?"
text_ataka_win = "Вы победили и получили 🌟 5 опыта.\n Вам выпало %s 💰"
text_ataka_lose = "Вы проиграли. Здоровье восстановится через 60 сек."
text_info_heroes = "Информация о герое %s\n" \
                   "id: %s\n" \
                   "👤 Игрок: %s\n"\
                   "🗺 Координаты: %s\n"\
                   "🏅 Уровень: %s \n" \
                   "🔋 Энергия: %s/%s\n" \
                   "🌟 Опыт: %s/%s\n" \
                   "❤ Здоровье: %s/%s\n\n" \
                   "Урон: %s\n\n" \
                   "🚶‍♂️Ур. ходьбы: %s (%s/%s)\n" \
                   "🚶‍♂️Ходов по карте: %s/%s\n\n" \
                   "💰 Золото: %s\n" \
                   "💎 Алмазы: %s\n"
text_info_storage = "Кол-во ресурсов на складе:\n⛏: %s ед.\n🌲: %s ед.\n⚒: %s ед.\n🌽: %s ед.\n💰: %s ед."

text_building_resource = "Уровень %s    %s \n\n " \
                         "Улучшить %s до %s уровня за: \n Камень: %s\n Дерево: %s\n Железо: %s\n Еда: %s"
# text_building_resource = "Строение %s \n %s уровень\n " \
#                         "Улучшить %s до %s уровня за: \n Камень: %s\n Дерево: %s\n Железо: %s\n Еда: %s"

text_building_market = "Ресурсы: \n💰 Золото: %s\n\n⛏ Камень: %s\n🌲 Дерево: %s\n⚒ Железо: %s\n🌽 Еда: %s\n\n\n" \
                       "Купить: \n⛏ Камень:  1💰/ 100⛏\n🌲 Дерево:  1💰/ 100🌲\n⚒ Железо:  1💰/ 100⚒\n🌽 Еда:          1💰/ 100🌽\n"

t_m = {"iron": {1: "маленький",
                2: "средний",
                3: "не большой",
                4: "большой",
                5: "огромный"},
       "wood": {1: "маленькому",
                2: "среднему",
                3: "не большому",
                4: "большому",
                5: "огромному"},
       "stone": {1: "маленький",
                 2: "средний",
                 3: "не большой",
                 4: "большой",
                 5: "огромный"}}


async def text_mining(user_id):
    text = ""
    row = await sql.sql_selectone("select * from resource where user_id = %s" % user_id)
    print(row)
    if row[7] == "iron":
        text = " 👣 Ты спустился в шахту и увидел %s кусок \n⛓ Металла.\n🏵 Уровень: %s\n❗ Количество ресурса: %s\n" \
               "⛏  Добыча: 2 штуки за 1 секунду.\n⏱ Сбор ресурса:  %s" % \
               (t_m[row[7]][row[8]], row[8], row[9],
                row[11])
    elif row[7] == "wood":
        text = " 👣 Ты подошел к %s стволу \n🌲 Дерева.\n🏵 Уровень: %s\n❗ Количество ресурса: %s\n" \
               "🪓  Добыча: 2 штуки за 1 секунду.\n⏱ Сбор ресурса:  %s" % \
               (t_m[row[7]][row[8]], row[8], row[9],
                row[11])
    elif row[7] == "stone":
        text = " 👣 Ты вошёл в пещеру и наткнулся на %s \n🧱 Булыжник.\n🏵 Уровень: %s\n❗ Количество ресурса: %s\n" \
               "⛏  Добыча: 2 штуки за 1 секунду.\n⏱ Сбор ресурса:  %s" % \
               (t_m[row[7]][row[8]], row[8], row[9],
                row[11])
    return text


text_training_uplvl = "Увеличьте уровень здания"
text_training_numwar = "\n Выберите кол-во войск"
text_training_castle = "У вас в замке:\n"
text_training_castle_old = "%s %s уровня: %s Потребляют - %s 🌽 \n"


text_location_all = "В замке: \n"

text_rename_nik = "Введите новый ник. Для отмены введите - 11"
text_shop = "Для подробной информации о товаре, нажмите на него"
text_shop_not_diamond = "У вас не хватает алмазов\n Приобрести можно тут /shop_master"
text_rename_nik_new = "Вы успешно сменили ник.\n Новый ник %s"
text_ref_up = "По вашей реф ссылке начислено %s 💎 "
text_ref_new = "По вашей рефссылке была регистрация"
text_top_heroes = "🥇 Топ по уровню\n \n"
text_top_castle = "🏰 Топ по замку\n \n"
text_moving_heroes = "Введите координаты в формате xx:xx\n Максимальное значение 100:100. \nДля отмены введите - 11"
text_moving_error = "Ввод не корректен, повторите в формате xx:xx.\n Для отмены введите - 11"
text_moving_win = "Вы были перемещены по координатам %s:%s"
text_moving_busy = "Ячейка занята, попробуйте другие координаты"
text_ataka_castle = "Вы напали на %s \nЧто будете делать?\n ⚔️Атаковать или 🏃‍♂️Отступить?"



button_maps = "🗺 Карта"
button_mining_map = "🗺 Вернуться на карту"
button_goto_two = "🏃‍♂ Отступить"
button_goto = "🏃‍♂ Сбежать"
button_castle_escape = "🏃🏻‍♂ Отступить"
button_castle_escape_field = "Покинуть поле боя"
list_Maps_goto = [button_maps,  button_goto_two,button_mining_map, button_mining,button_goto,button_castle_escape, button_castle_escape_field,"/--", "⏱ Вывод карты ⏱"]
list_Maps = [button_maps,button_goto_two,button_castle_escape,button_goto,button_castle_escape_field,"🗺 Вернуться на карту", '🗺 Карта']




