import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

REMOTE_HOST = os.getenv('REMOTE_HOST')
TCP_PORT = os.getenv('TCP_PORT')

VALID_KEY = os.getenv('TCP_VALID_MASTER_KEY')


async def tcp_client(message):
    reader, writer = await asyncio.open_connection(REMOTE_HOST, TCP_PORT)
    logger.info(f"Connected to server at {REMOTE_HOST}:{TCP_PORT}")

    auth_key = "test"

    # 인증키 전송
    writer.write(auth_key.encode() + b'\n')
    await writer.drain()

    # 인증 결과 수신
    auth_response = await reader.read(100)

    # 인증 실패 시 처리
    if b"Authentication successful" not in auth_response:
        logger.error("Authentication failed, closing connection")
        writer.close()
        await writer.wait_closed()
        return

    # 인증 성공 시 처리
    logger.info("Authentication successful")

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
