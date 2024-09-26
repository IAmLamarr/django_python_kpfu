from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sqlite3
from collections import Counter
import pprint

COLLISION_NUM = 9_424_334
LIMIT = 100_000
offsets = range(0, COLLISION_NUM, LIMIT)

con = sqlite3.connect('database.db')
cursor = con.cursor()

def process_data(offset):
    expression = f"SELECT weather_1, COUNT(*) FROM (SELECT * FROM collisions LIMIT {LIMIT} OFFSET {offset}) GROUP BY weather_1"
    print(expression)
    data = cursor.execute(expression)
    data = Counter(dict(data))
    return data

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_data, offsets))
        pprint.pprint(results)

