import asyncio
import random
import time

async def get_temperature(city: str):
    await asyncio.sleep(2)
    temp = random.randint(10, 20)
    return f'В городе {city} {temp} градусов'

async def main():
    cities = ['Москва', 'Питер', 'Казань']

    await asyncio.gather(
        *[get_temperature(city) for city in cities]
    )

if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())
    end = time.time()

    diff = round(end - start)
    print(f"Отработало за {diff} с.")
