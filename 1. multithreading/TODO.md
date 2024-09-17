# Поисковая система 

Написать программу, которая будет искать вхождение некоторого слова в описании статьей всех компаний в Хабре

TODO:
- Сделать программу получения всех компаний из Хабра
    - Ускорить программу через threading
- Сделать программу получения текстов постов для некоторой компании
    - Ускорить программу через threading

Список компаний
https://habr.com/ru/companies/page{{page}}/

Например:
https://habr.com/ru/companies/page1/
https://habr.com/ru/companies/page2/
https://habr.com/ru/companies/page3/

Список статей для компании:
https://habr.com/ru/rss/companies/{{company}}/articles/?fl=ru&limit=1000

Например:
https://habr.com/ru/rss/companies/avito/articl es/?fl=ru&limit=1000
https://habr.com/ru/rss/companies/alfa/articles/?fl=ru&limit=1000
