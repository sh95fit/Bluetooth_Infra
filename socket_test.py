import asyncio


async def tcp_client(message):
    reader, writer = await asyncio.open_connection('131.186.19.64', 83)

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
