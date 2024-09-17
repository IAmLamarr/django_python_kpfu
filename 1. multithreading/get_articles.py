import requests
import json
import time
import math
import threading

json_companies = json.load(open('companies.json', 'r'))

SEARCH_WORD = "интерфейс"
THREADS = 160

def search_word_by_company(company, word):
    req = requests.get(f"https://habr.com/ru/rss/companies/{company}/articles/?fl=ru&limit=100")

    text = req.text

    count = text.lower().count(word)

    current_thread = threading.current_thread()
    thread_name = current_thread.name

    print(f'({thread_name}) {company}: {count}')

def search_word_by_company_pool(company_pool, word):
    for company in company_pool:
        search_word_by_company(company, word)

start = time.time()

companies = list(json_companies.keys())
companies_len = len(companies)
thread_pool_length = math.ceil(companies_len / THREADS)

threads = []

for thread_num in range(THREADS):
    left_border = thread_num * thread_pool_length
    rigth_border = min(left_border + thread_pool_length + 1, companies_len)
    pool = companies[left_border:rigth_border]
    thread = threading.Thread(
        name=thread_num + 1,
        target=search_word_by_company_pool,
        args=(pool, SEARCH_WORD)
    )
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.time()
diff = round(end - start, 1)

print(f"Поиск по статьям занял {diff} секунд")
