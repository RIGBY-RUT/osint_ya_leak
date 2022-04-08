#!/usr/bin/env python3



import csv


import re
import pandas
#import pandas as pd

import config

import pathlib, threading, time, queue

def worker(que, rex, where, df_all):
    result = ''
    while True:
        # Получаем задание (имя файла) из очереди
        job = que.get()
        task = ''

        # открываем файл из очереди на чтение
        with open(job, 'r', encoding='utf-8') as fr:

            #for string in fr.readlines():
            #    if re.match(rex, string):
            #        task = string
            #        print(task)
            #        df_all.join(task)

            #print(job)
            df = pandas.read_csv(job, low_memory=False, dtype='unicode')
            #df = df.dropna()
            #print ("After applying ", rex, " DataFrame is:\n", df[df['full_name'].str.contains(rex) ])
            #result = (df[df['full_name'].str.contains(rex, na=False)]).to_string(index=False, header=False)
            result = df[df['full_name'].str.contains(rex, na=False)]
            #result = df['full_name'].str.extract(r"+rex+")


            #found = [df.str.contains(rex, na=False)]
            #result = result.DataFrame.to_csv


            print('--' * 20)
            print(result.to_string(index=False, header=False))
            frames = [df_all, result]
            df_all = pandas.concat(frames)
            print('==' * 20)
            print(df_all.to_string(index=False, header=False))

            #if not 'Empty DataFrame' in result:
            #    print('--'*20)
            #    print(result)
            #    df_all.append(result)




            #print(result)
            #df_all += df.loc[0]
            #if str(result.value_counts()) != 'Series([], dtype: int64)':
            #    df_all += df.loc[0]
            #    print(df_all)
        #print(df_all)
        que.task_done()
        #print(result.value_counts())
        #return ()

def find_name(name, where):
    df_all = pandas.DataFrame()


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

    for file in list_files:
        #print(file)
        que.put(file)

    if que.qsize():
        # Создаем и запускаем потоки
        n_thead = 8

        for _ in range(n_thead):
            th = threading.Thread(target=worker, args=(que, rex, where, df_all), daemon=True)
            th.start()

            print (th)
        # Блокируем дальнейшее выполнение
        # программы до тех пор пока потоки
        # не обслужат все элементы очереди
        que.join()
        print('+++++++++++++++++++++++++++++++++++++++++++++')
        print(df_all.to_string(index=False, header=False))
        return df_all;
    else:
        print('Файлы не найдены.')
    print('++++++++++++++++++++++++++++++')
    print(df_all)

find_name("Сосновый", "full_name")