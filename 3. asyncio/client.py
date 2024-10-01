import asyncio
from utils import *
import aioconsole

async def handle_print(reader: asyncio.StreamReader):
    while True:
        received = await read_data(reader)
        await aioconsole.aprint(received)

async def handle_input(writer: asyncio.StreamWriter):
    while True:
        msg = await aioconsole.ainput()
        await write_data(writer, msg)

async def main():
    host = SOCKET_HOST
    port = SOCKET_PORT
    reader, writer = await asyncio.open_connection(
        host=host, 
        port=port
    )

    print(f'Connected to {host}:{port}')

    username = input("Enter your username: ")
    await write_data(writer, username)

    asyncio.create_task(handle_print(reader))
    await handle_input(writer)


if __name__ == "__main__":
    asyncio.run(main())