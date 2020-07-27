import threading
import time
from work.Map import timer_start
from utils import sql
from datetime import datetime
from work.Users import start_user_default
import asyncio


async def schedule_farm():
    print("farm")
    while 1 < 2:
        await asyncio.sleep(60)
        rows = await sql.sql_select("select user_id from heroes")
        for row in rows:
            request = f"""SELECT null_old, farm_timer, resource.food
    FROM heroes, resource  
    INNER JOIN building ON heroes.farm = building.lvl
    WHERE data_old = 'farm' AND heroes.user_id = {row[0]} and resource.user_id = {row[0]}"""
            # print(request)
            production, farm_time, food = await sql.sql_selectone(request)
            farm_time_old = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            a = farm_time_old.split(':')
            aa = datetime(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]))
            b = farm_time.split(':')
            bb = datetime(int(b[0]), int(b[1]), int(b[2]), int(b[3]), int(b[4]), int(b[5]))
            ss = int((aa - bb).seconds / 2)
            consumption = 0
            user_id = row[0]
            request = f"""SELECT stable + barracks + shooting, consumption FROM warrior INNER JOIN training
                      ON warrior.lvl=training.lvl WHERE warrior.user_id = {user_id} and name = 'stable'"""
            # print(request)
            rows = await sql.sql_select(request)
            for row in rows:
                consumption += row[0] * row[1]
            num_farm = production * ss - consumption
            food += num_farm
            if food < 0:
                update = (f"update resource set food = 0, farm_timer = '{farm_time_old}' where user_id = {user_id}")
                await sql.sql_insert(update)
            else:
                update = (
                    f"update resource set food = {food}, farm_timer = '{farm_time_old}' where user_id = {user_id}")
                await sql.sql_insert(update)
        # if num_farm <= 0:
        #     update = ("update resource set food = food - %s, farm_timer = '%s' "
        #               "where user_id = %s" % (num_farm, farm_time_old, user_id))
        #     sql.sql_insertscript_no_await(update)
        # else:
        #     update = ("update resource set food = food + %s, farm_timer = '%s' "
        #               "where user_id = %s" % (num_farm, farm_time_old, user_id))
        #     sql.sql_insertscript_no_await(update)
        #
        # food = sql.sql_selectone_no_await(f"SELECT food FROM resource WHERE user_id = {user_id}")[0]
        #

    #     lvl_storage = build[str(k)]["storage"]
    #     num_storage = int(buildings["storage"][lvl_storage]["capacity"])
    #     if resource[str(k)]["food"] + num_farm - min > num_storage:
    #         resource[str(k)]["food"] = num_storage
    #     elif resource[str(k)]["food"] + num_farm - min < 0:
    #         resource[str(k)]["food"] = 0
    #     else:
    #         resource[str(k)]["food"] += num_farm - min
    #    resource[str(k)]["farm_time"] = farm_time_old


# def farm_timer():
#     print("Фарм")
#     schedule.every(1).minutes.do(schedule_farm)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


async def all():
    # await timer_start()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(timer_start())
    # loop.run_until_complete(start_user_default())
    # loop.run_until_complete(schedule_farm())

    asyncio.ensure_future(timer_start())
    asyncio.ensure_future(start_user_default())
    asyncio.ensure_future(schedule_farm())
    # loop.run_forever()
    # await timer_start()
    # await start_user_default()
    # await schedule_farm()
    # threading.Thread(target=timer_start).start()
    # threading.Thread(target=farm_timer).start()
