import asyncio
import ssl
import logging
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from celery import Celery
from Data_Encryption import RSA_Utils
from Parser import Len120

print(os.getcwd())

load_dotenv()

HOST = os.getenv('TCP_HOST')
PORT = os.getenv('TCP_PORT')

# MONGO_URI = os.getenv('MONGO_URI')
# MONGO_DB = os.getenv('MONGO_DB')
# MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME')

VALID_KEY = os.getenv('TCP_VALID_MASTER_KEY')
RSA_KEY_PASSWORD = os.getenv('RSA_KEY_PASSWORD')

# MongoDB 클라이언트 설정
# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB]
# collection = db[MONGO_COLLECTION_NAME]


# 로그 디렉토리 생성 (디렉토리가 없으면 생성)
os.makedirs('/var/log/socketserver', exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/socketserver/server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


celery_app = Celery('socketserver',
                    broker=os.getenv('CELERY_BROKER_URL'))


private_key = RSA_Utils.load_private_key(
    './Data_Encryption/private_test_key.pem', RSA_KEY_PASSWORD)


# TCP 연결 전 인증 절차 추가
# KEY 인증에 성공한 장비만 연결 허용
async def authenticate(reader, writer):
    # 클라이언트가 인증키를 전송할 때까지 기다림
    encrypted_data = await reader.read(256)
    decrypted_data = RSA_Utils.decrypt_with_private_key(
        private_key, encrypted_data).strip()
    auth_key = decrypted_data.strip()

    if auth_key == VALID_KEY:
        writer.write(b"Authentication successful\n")
        await writer.drain()
        return True
    else:
        writer.write(b"Authentication failed\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return False


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logger.info(f"Connected to {addr}")
    print(f"Connected to {addr}")

    if not await authenticate(reader, writer):
        logger.info(f"Authentication failed for {addr}")
        return

    try:
        while True:
            encrypted_data = await reader.read(256)

            if len(encrypted_data) == 0:
                logger.info(
                    f"Empty data received from {addr}. Closing connection.")
                break

            data = RSA_Utils.decrypt_with_private_key(
                private_key, encrypted_data)
            if not data:
                break
            message = data

            try:
                # collection.insert_one(message_data)
                # logger.info(f"Inserted document: {message_data}")

                # collection.insert_one({
                #     'address': str(addr),
                #     'message': message
                # })
                celery_app.send_task(
                    'tasks.save_to_mongodb.save_data_to_mongo', args=[addr, message])
                logger.info(f"Inserted document: {message}")
            except Exception as e:
                logger.error(f"Error inserting document into MongoDB: {e}")

            try:
                # 테스트용 데이터 (json 형태의 데이터 불러오기 + 주소값 추가)
                # message_data = json.loads(message)
                # message_data['address'] = str(addr)

                # 실 데이터
                real_data = json.loads(data)
                if len(real_data['message']) == 120:
                    real_data['length'] = 120
                    real_data['address'] = str(addr)
                    parser_message = Len120.data_parser(real_data['message'])
                    real_data.update(parser_message)
                    logger.info(f"Real data : {real_data}")
                else:
                    logger.info(f"Data length mismatch, exception handled")

                # 테스트용 데이터 수집 Task
                # celery_app.send_task('tasks.save_to_mysql_test.save_data_to_db',
                #                      args=[message_data])

                # 실 데이터 수집 Task
                celery_app.send_task('tasks.save_to_mysql.save_data_to_db',
                                     args=[real_data])

                logger.info(f"Celery Task Success")
            except Exception as e:
                logger.error(f"Error sending task to Celery : {e}")

            logger.info(f"{addr} : {message}")
            # logger.info(f"Send: {message}")
            writer.write(b"Success All Process")
            await writer.drain()

    except asyncio.CancelledError:
        logger.warning(f"Connection with {addr} was cancelled")

    except Exception as e:
        logger.error(f"Error with {addr}: {e}")

    finally:
        logger.info(f"Closing the connection with {addr}")
        writer.close()
        await writer.wait_closed()


async def main():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(
        certfile='server_test.crt', keyfile='server_test.key')

    server = await asyncio.start_server(handle_client, HOST, PORT, ssl=ssl_context)
    # server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
