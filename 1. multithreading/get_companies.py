import requests
import bs4
import pprint
import time
import json

companies = dict()
pages = 19

def get_companies_from_page(page):
    print(f"Скачиваем страницу {page}")
    req = requests.get(f"https://habr.com/ru/companies/page{page}/")

    text = req.text

    parser = bs4.BeautifulSoup(text, features="html.parser")

    links = parser.find_all('a', attrs={
        'data-test-id': 'company-title'
    })

    for link in links:
        url = str(link['href'])
        company = link.text

        alias = url.replace("/ru/companies/", "").replace('/profile/', '')

        companies[company] = alias

start = time.time()


for page in range(1, pages + 1):
    get_companies_from_page(page)


end = time.time()

diff = round(end - start, 1)

pprint.pprint(companies)

print(f"Загрузка заняла {diff} секунд")

json_companies = json.dumps(
    companies,
    indent=4,
    ensure_ascii=False,
)

file = open("companies.json", 'w')

file.write(json_companies)

file.close()