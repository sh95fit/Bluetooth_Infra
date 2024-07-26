import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

REMOTE_HOST = os.getenv('REMOTE_HOST')
TCP_PORT = os.getenv('TCP_PORT')


async def tcp_client(message):
    reader, writer = await asyncio.open_connection(REMOTE_HOST, TCP_PORT)

    print(f'Send: {message}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main():
    messages = ['Hello World!', 'This is a test message.', 'Another message.']
    for message in messages:
        await tcp_client(message)

asyncio.run(main())
