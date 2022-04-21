# osint_ya_leak

![This is an image](https://github.com/RIGBY-RUT/osint_ya_leak/blob/adc9ce64757f4f15f316cd4c71381f9442ce6f0f/%D0%91%D0%B5%D0%B7%20%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8.png)

В репозитории предоставлен скрипт для поиска информации в БД mongodb, через бота в Telegram.

Для запуска необходимо:
* установить все зависимости из [requirements.txt](https://github.com/RIGBY-RUT/osint_ya_leak/blob/4c67b3bd8ce173902ae7da03573371af692ab7ef/requirements.txt) для python3, 
* Telegram token прописать в файле config.py,
* Mongodb должна содержать данные из утечки Yandex delivery в формате представленом в [BD_emulator.py](https://github.com/RIGBY-RUT/osint_ya_leak/blob/e9aa059a6c4f599439b67e999aeed830a16311ce/BD_emulator.py) (желательно избавиться от паразитных символов ',' и '"'). Для добавления из CLI можно воспользоваться ```for file in ../sourse/*; do   mongoimport --host=127.0.0.1 -d Ya_leaks -c mod_3 --type csv --file "$file" --headerline;   done```. В случае, если есть необходимость поиска в файлах, можно воспользоватся одним из скриптов Ya_found_*.

Telegram bot поддерживает вледующий тип запросов:
* ввод email в формате (^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$) - поиск по email;
* ввод номера мобильного телефона (^([+]?[0-9\s-\(\)]{3,25})*$) - поиск по телефону;
* ввод ФИО или части ФИО;
* /start - диалог для поиска по конкретному полю таблицы.

При поиске в БД, используется формат regexp ".\*<искомое>.\*".
В случае наличия координат заказа, пользователю будет отправлена карта с указанием места доставки заказа.




TO_DO - поиск кодов для открытия домофонов по геопозиции
