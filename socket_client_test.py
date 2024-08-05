import socket
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
TCP_PORT = int(os.getenv('TCP_PORT'))

VALID_KEY = os.getenv('TCP_VALID_MASTER_KEY')


public_key = RSA_Utils.load_public_key(
    './SocketServer/Data_Encryption/public_test_key.pem')

TIMEOUT = 10


def tcp_client(message):

    # SSL/TLS 설정
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        ssl_client_socket = ssl_context.wrap_socket(
            client_socket, server_hostname=REMOTE_HOST)

        ssl_client_socket.connect((REMOTE_HOST, TCP_PORT))
        print("서버와 연결되었습니다.")

        auth_key = VALID_KEY
        encrypted_auth_key = RSA_Utils.encrypt_with_public_key(
            public_key, auth_key)

        try:
            ssl_client_socket.send(encrypted_auth_key)
            print("인증키가 정상적으로 전송되었습니다.")

            auth_response = ssl_client_socket.recv(1024)
            print('Received', repr(auth_response.decode()))

            # 인증 실패 시 처리
            if b"Authentication successful" not in auth_response:
                logger.error("Authentication failed, closing connection")
                ssl_client_socket.close()
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

            ssl_client_socket.send(encrypted_json_data)
            print(f'Send >> {send_time} : {message}')

            response = ssl_client_socket.recv(1024)
            print('Received', repr(response.decode()))

            ssl_client_socket.close()
            print('Close the connection')

        except:
            print("인증키 전송에 실패했습니다.")

        ssl_client_socket.close()
    except ConnectionRefusedError:
        print("서버와 연결할 수 없습니다.")


def main():
    messages = ['This is a socket module test message.']
    for message in messages:
        tcp_client(message)


if __name__ == "__main__":
    main()
