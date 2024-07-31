import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import logging
import ssl
from SocketServer.Data_Encryption import RSA_Utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

REMOTE_HOST = os.getenv('REMOTE_HOST')
TCP_PORT = os.getenv('TCP_PORT')

VALID_KEY = os.getenv('TCP_VALID_MASTER_KEY')


public_key = RSA_Utils.load_public_key(
    './SocketServer/Data_Encryption/public_test_key.pem')

TIMEOUT = 10


async def tcp_client(message):

    # SSL/TLS 설정
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    reader, writer = await asyncio.open_connection('127.0.0.1', TCP_PORT, ssl=ssl_context)
    logger.info(f"Connected to server at {REMOTE_HOST}:{TCP_PORT}")

    auth_key = VALID_KEY
    encrypted_auth_key = RSA_Utils.encrypt_with_public_key(
        public_key, auth_key)

    # 인증키 전송
    writer.write(encrypted_auth_key)
    # logger.info(
    #     f"Encrypted auth key: {encrypted_auth_key} / {len(encrypted_auth_key)}")
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
    encrypted_json_data = RSA_Utils.encrypt_with_public_key(
        public_key, json_data)

    print(f'Send >> {send_time} : {message}')
    writer.write(encrypted_json_data)
    # logger.info(
    #     f"Encrypted json_data: {encrypted_json_data} / {len(encrypted_json_data)}")

    # response = await reader.read(256)
    response = await asyncio.wait_for(reader.read(256), timeout=TIMEOUT)
    print(f'Received: {response.decode()}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main():
    messages = ['This is a test message.']
    for message in messages:
        await tcp_client(message)

asyncio.run(main())
