import asyncio
import csv
import pathlib
import re

import aiofiles
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter


#############################################

#!/usr/bin/env python3



import csv


import re
import pandas

import config

import pathlib, threading, time, queue

async def founding(file, rex, df_all):
    # simple reading
    async with aiofiles.open(file, mode="r", encoding="utf-8", newline="") as afp:
        print(file)
        async for row in AsyncReader(afp):
            #print(row[2])
            if re.match(rex, row[2]):
                task = row
                print(task)
                df_all.join(task)

def worker(que, rex, df_all):
    result = ''
    while True:
        # Получаем задание (имя файла) из очереди
        job = que.get()
        task = ''

        # открываем файл из очереди на чтение
        async with aiofiles.open(file, mode="r", encoding="utf-8", newline="") as afp:
            print(file)
            async for row in AsyncReader(afp):
                # print(row[2])
                if re.match(rex, row[2]):
                    task = row
                    print(task)
                    df_all.join(task)

            #print(job)
            #df = pandas.read_csv(job, low_memory=False, dtype='unicode')
            #df = df.dropna()
            #print ("After applying ", rex, " DataFrame is:\n", df[df['full_name'].str.contains(rex) ])
            #result = df.loc[df['full_name'].str.contains(rex, na=False) ]
            #df_all = df_all.append(result, ignore_index=True)
            #if str(result.value_counts()) != 'Series([], dtype: int64)':

                #print(result.value_counts())
        #print(df_all)
        que.task_done(df_all)
        #print(result.value_counts())
        #return ()

def find_name(name):
    path = pathlib.Path('.')
    # тестовый каталог с файлами
    test_dir = 'C:\\Users\\msosnoviy\\PycharmProjects\\telebot\\data_source'
    # Путь к тестовой директории
    path_dir = path.joinpath(test_dir)

    # получаем список файлов
    list_files = path_dir.glob('*.csv')
    # каталог с обработанными файлами
    #test_dir_modified = 'test_dir_modified'
    #path_dir_modified = path.joinpath(test_dir_modified)
    #path_dir_modified.mkdir(exist_ok=True)

    # создаем и заполняем очередь именами файлов
    que = queue.Queue()
    rex = str('.*' + name + '.*')
    #print (rex)
    df_all=''
    for file in list_files:
        #print(file)
        que.put(file)

    if que.qsize():
        # Создаем и запускаем потоки
        n_thead = 10
        df_all=''
        for _ in range(n_thead):
            th = threading.Thread(target=worker, args=(que, rex, df_all), daemon=True)
            th.start()
            print (th)
        # Блокируем дальнейшее выполнение
        # программы до тех пор пока потоки
        # не обслужат все элементы очереди
        que.join()
        print(df_all)
        return df_all;
    else:
        print('Файлы не найдены.')

find_name("Сосновый")

#############################################



#async def runer(file, rex, df_all):




async def founding(file, rex, df_all):
    # simple reading
    async with aiofiles.open(file, mode="r", encoding="utf-8", newline="") as afp:
        print(file)
        async for row in AsyncReader(afp):
            #print(row[2])
            if re.match(rex, row[2]):
                task = row
                print(task)
                df_all.join(task)
            #print(row)  # row is a list

    # dict reading, tab-separated


def main():

    path = pathlib.Path('.')
    # тестовый каталог с файлами
    test_dir = 'C:\\Users\\msosnoviy\\PycharmProjects\\telebot\\data_source'
    # Путь к тестовой директории
    path_dir = path.joinpath(test_dir)

    # получаем список файлов
    list_files = path_dir.glob('*.csv')
    name = 'Сосновый'
    rex = str('.*' + name + '.*')
    # print (rex)
    df_all = ''

    for file in list_files:
        asyncio.run(founding(file, rex, df_all))




import asyncio

def read_file(file_name):
    return open(file_name).read()

async def main():
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, read_file, 'data.txt')
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())