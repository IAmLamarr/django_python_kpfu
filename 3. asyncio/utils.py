import dotenv
import asyncio
import os

dotenv.load_dotenv()
SOCKET_HOST = os.getenv('SOCKET_HOST')
SOCKET_PORT = os.getenv('SOCKET_PORT')

ENCODING = 'utf-8'

async def write_data(writer: asyncio.StreamWriter, data: str):
    with_space = data + '\n'
    writer.write(with_space.encode(encoding=ENCODING))
    await writer.drain()

async def read_data(reader: asyncio.StreamReader):
    byte_data = await reader.readline()
    return str(byte_data, encoding=ENCODING)[:-1]