import asyncio
import pprint
import uuid
from utils import *

usernames = dict()
async_hadlers = dict()

async def send_message(user_uuid: str, msg: str):
    reader, writer = async_hadlers[user_uuid]
    await write_data(writer, msg)

async def broadcast(user_uuid: str):
    while True:
        reader, writer = async_hadlers[user_uuid]
        msg = await read_data(reader)
        username = usernames[user_uuid]

        print(f'New message from {username}: {msg}')

        for user in usernames:
            if user != user_uuid:
                msg_with_user = f'[{username}] {msg}'
                await asyncio.create_task(send_message(user, msg_with_user))
    

async def server_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    username = await read_data(reader)
    user_uuid = str(uuid.uuid4())

    usernames[user_uuid] = username
    async_hadlers[user_uuid] = (reader, writer)

    print(f'New user registered: {username}')
    pprint.pprint(usernames)

    await broadcast(user_uuid)

async def main():
    host = SOCKET_HOST
    port = SOCKET_PORT
    server = await asyncio.start_server(
        server_handler, 
        host=host, 
        port=port,
    )

    print(f'Server running at {host}:{port}')

    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())