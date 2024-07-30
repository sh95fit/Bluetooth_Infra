import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

REMOTE_HOST = os.getenv('REMOTE_HOST')
TCP_PORT = os.getenv('TCP_PORT')


async def tcp_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', TCP_PORT)

    send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'send_time': send_time,
        'message': message
    }

    json_data = json.dumps(data)

    print(f'Send >> {send_time} : {message}')
    writer.write(json_data.encode())

    response = await reader.read(300)
    print(f'Received: {response.decode()}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main():
    messages = ['This is a test message.']
    for message in messages:
        await tcp_client(message)

asyncio.run(main())
