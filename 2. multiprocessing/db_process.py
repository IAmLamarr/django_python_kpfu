import sqlite3
import pprint
import time
import math
import threading
import os
from collections import Counter
import multiprocessing

con = sqlite3.connect('database.db')
cursor = con.cursor()

def threading_func(offset, limit):
    expression = f"SELECT weather_1, COUNT(*) FROM (SELECT * FROM collisions LIMIT {limit} OFFSET {offset}) GROUP BY weather_1"
    print(expression)
    data = cursor.execute(expression)
    data = Counter(dict(data))

def process_solution():
    COLLISION_NUM = 9_424_334
    PROCESS_NUM = os.cpu_count() // 2
    start = time.time()
    limit = math.ceil(COLLISION_NUM / PROCESS_NUM)

    processes = []

    for proccess_num in range(PROCESS_NUM):
        offset = proccess_num * limit
        process = multiprocessing.Process(
            name=str(proccess_num),
            target=threading_func,
            args=(offset, limit)
        )
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    end = time.time()
    diff = round(end - start, 1)

    # pprint.pprint(global_data.most_common(3))

    print(f"Обработка процессами ({PROCESS_NUM}) заняла {diff} секунд")

if __name__ == "__main__":
    process_solution()