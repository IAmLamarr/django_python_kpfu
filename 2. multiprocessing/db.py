import sqlite3
import pprint
import time
import math
import threading
from collections import Counter

# SELECT - найти
# FROM - откуда
# SELECT <данные> FROM <table>
# WHERE - фильтруем по условию
# SELECT <данные> FROM <table> WHERE <условие>
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(cursor.fetchall())

# PRAGMA table_info(<table>) - вывести структуру БД
# cursor.execute("PRAGMA table_info(collisions)")
# pprint.pprint(cursor.fetchall())

# 9424334
# LIMIT - ограничение кол-ва возвращаемых записей
# OFFSET - "сдвиг" курсора

# 1 - 0 - 100 LIMIT 100 OFFSET 0
# 2 - 100 - 200 LIMIT 100 OFFSET 100
# 3 - 200 - 300 LIMIT 100 OFFSET 200
# cursor.execute("SELECT case_id FROM (SELECT case_id FROM collisions LIMIT 10 OFFSET 15)")
# pprint.pprint(cursor.fetchall())

# cursor.execute("SELECT weather_1 FROM collisions")
# pprint.pprint(cursor.fetchall())

# При какой погоде (weather_1) чаще всего происходили аварии?
def simple_solution():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    start = time.time()
    cursor.execute("SELECT weather_1, COUNT(*) FROM collisions GROUP BY weather_1")
    data = cursor.fetchall()
    end = time.time()

    diff = round(end - start, 1)
    pprint.pprint(dict(data))
    print(f"Запрос занял {diff} сек")

lock = threading.Lock()
global_data = Counter()

def threading_func(offset, limit):
    global global_data
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    expression = f"SELECT weather_1, COUNT(*) FROM (SELECT * FROM collisions LIMIT {limit} OFFSET {offset}) GROUP BY weather_1"
    # print(expression)
    data = cursor.execute(expression)
    data = Counter(dict(data))

    lock.acquire()
    global_data += data
    lock.release()

# Хочется распараллелить нагрузку по ядрам, для этого разделим задачу на процессы
# Если работаем с вводом/выводом инфы - потоки
# Если работаем с большим кол-вом вычислений - надо разделять на потоки
# 1 процесс обрабатывает 1 ядро процессора
# 1 тред == 1 процесс
def thread_solution():
    COLLISION_NUM = 9_424_334
    THREAD = 10
    start = time.time()
    limit = math.ceil(COLLISION_NUM / THREAD)

    threads = []

    for thread_num in range(THREAD):
        offset = thread_num * limit
        thread = threading.Thread(
            name=thread_num + 1,
            target=threading_func,
            args=(offset, limit)
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()
    diff = round(end - start, 1)

    pprint.pprint(global_data.most_common(3))

    print(f"Обработка потоками ({THREAD}) заняла {diff} секунд")

if __name__ == "__main__":
    thread_solution()