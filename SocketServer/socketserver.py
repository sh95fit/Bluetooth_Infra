import asyncio
# import ssl
import logging
import os

HOST = '0.0.0.0'
PORT = 83

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


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logger.info(f"Connected to {addr}")
    print(f"Connected to {addr}")

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            print(f"Received {message} from {addr}")

            print(f"Send: {message}")
            writer.write(data)
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
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # server = await asyncio.start_server(handle_client, HOST, PORT, ssl=ssl_context)
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
