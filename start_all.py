import threading
import schedule
import time
from Map import timer_start
import sql
from datetime import datetime
from Users import start_user_default

# Параметры при старте





def sheduler_farm():
    rows = sql.sql_select_no_await("select user_id from heroes")
    for row in rows:
        request = f"""SELECT null_old, farm_timer 
FROM heroes, resource  
INNER JOIN building ON heroes.farm = building.lvl
WHERE data_old = 'farm' AND heroes.user_id = {row[0]} and resource.user_id = {row[0]}"""
        production, farm_time = sql.sql_selectone_no_await(request)
        farm_time_old = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        a = farm_time_old.split(':')
        aa = datetime(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]))
        b = farm_time.split(':')
        bb = datetime(int(b[0]), int(b[1]), int(b[2]), int(b[3]), int(b[4]), int(b[5]))
        ss = int((aa - bb).seconds / 2)
    #     war_1 = warrior[str(k)]["shooting"]["1"] + warrior[str(k)]["barracks"]["1"] + warrior[str(k)]["stable"]["1"]
    #     war_2 = warrior[str(k)]["shooting"]["2"] + warrior[str(k)]["barracks"]["2"] + warrior[str(k)]["stable"]["2"]
    #     war_3 = warrior[str(k)]["shooting"]["3"] + warrior[str(k)]["barracks"]["3"] + warrior[str(k)]["stable"]["3"]
    #     min = int(ss * war_1 / 60 + ss * war_2 * 3 / 60 + ss * war_3 * 5 / 60)

        num_farm = production * ss
        update = ("update resource set food = food + %s, farm_timer = '%s' "
                  "where user_id = %s" % (num_farm, farm_time_old, row[0]))
        sql.sql_insertscript_no_await(update)
    #     lvl_storage = build[str(k)]["storage"]
    #     num_storage = int(buildings["storage"][lvl_storage]["capacity"])
    #     if resource[str(k)]["food"] + num_farm - min > num_storage:
    #         resource[str(k)]["food"] = num_storage
    #     elif resource[str(k)]["food"] + num_farm - min < 0:
    #         resource[str(k)]["food"] = 0
    #     else:
    #         resource[str(k)]["food"] += num_farm - min
    #    resource[str(k)]["farm_time"] = farm_time_old


def farm_timer():
    print("Фарм")
    schedule.every(1).minutes.do(sheduler_farm)
    while True:
        schedule.run_pending()
        time.sleep(1)


async def all():
    threading.Thread(target=timer_start).start()
    threading.Thread(target=farm_timer).start()
    await start_user_default()

