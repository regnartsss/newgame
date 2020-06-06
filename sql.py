import sqlite3

import logging
from load_all import benchmark
import os
def find_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).replace('\\', '/') + '/'

PATH = find_location()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

# @benchmark
async def sql_insert(request):
    # print(request)
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    conn.commit()
    conn.close()

# @benchmark
async def sql_insertscript(request):
    # print(request)
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()

    cursor.executescript(request)
    conn.commit()
    conn.close()
# @benchmark
async def sql_select(request):
    # print(request)
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchall()
    return rows

# @benchmark
async def sql_selectone(request):
    # print(request)
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchone()
    return rows


def sql_select_no_await(request):
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchall()
    return rows


def sql_insertscript_no_await(request):
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.executescript(request)
    conn.commit()
    conn.close()

def sql_selectone_no_await(request):
    conn = sqlite3.connect(PATH+'database.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchone()
    return rows