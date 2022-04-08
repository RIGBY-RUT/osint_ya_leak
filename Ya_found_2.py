import pandas



####
#Where can be phone_number;first_name;full_name;email;address_city,address_street,address_house,address_entrance
####
def worker(rex, where):
    result = ''
    while True:
        # Получаем задание (имя файла) из очереди
        job = 'yandex_eda.csv'
        task = ''

        # открываем файл из очереди на чтение
        #with open(job, 'r', encoding='utf-8') as fr:
        df = pandas.read_csv('yandex_eda.csv', low_memory=False, dtype='unicode', on_bad_lines='skip', delimiter=';')
        #df = df.dropna()
        #print ("After applying ", rex, " DataFrame is:\n", df[df['full_name'].str.contains(rex) ])
        result = df.loc[df[where].str.contains(rex, na=False) ]
        #df_all = df_all.append(result, ignore_index=True)
        if str(result.value_counts()) != 'Series([], dtype: int64)':

            print(result.value_counts())
        #print(df_all)
        #que.task_done()
        #print(result.value_counts())
        return (str(result.value_counts()))

