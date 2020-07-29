import sqlite3
import logging
import os



def find_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).replace('\\', '/') + '/'


PATH = find_location()
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')


async def sql_insert(request):
    conn = sqlite3.connect(PATH + 'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    conn.commit()
    conn.close()


async def sql_insert_conn(request):
    conn = sqlite3.connect(PATH + 'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    conn.commit()


async def sql_insertscript(request):
    conn = sqlite3.connect(PATH + 'database.db')
    cursor = conn.cursor()
    cursor.executescript(request)
    conn.commit()
    conn.close()


async def sql_select(request):
    conn = sqlite3.connect(PATH + 'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchall()
    return rows


async def sql_selectone(request):
    conn = sqlite3.connect(PATH + 'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchone()
    return rows
