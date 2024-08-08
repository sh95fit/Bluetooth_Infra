import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "19fa165e-dfe4-44ac-a518-1e71feae6900"
CHARACTERISTIC_UUID = "73c66424-9ace-492d-beb6-239ba04bdbf2"


async def run_client():
    print("Scanning for device...")

    try:
        devices = await BleakScanner.discover()
    except Exception as e:
        print(f"Error during device discovery: {e}")
        return

    target_device = None

    for device in devices:
        print(f"Found device: {device.name} : {device.address}")
        if SERVICE_UUID in device.metadata.get("uuids", []):
            target_device = device
            break

    if target_device is None:
        print("No device with the required service UUID found")
        return

    try:
        async with BleakClient(target_device) as client:
            print(f"Connected to {device.name}")

            # 데이터 전송
            message = "Bluetooth Test Data"
            await client.write_gatt_char(CHARACTERISTIC_UUID, message.encode())
            print(f"Sent: {message}")

            # 서버 측으로부터 응답 읽기
            response = await client.read_gatt_char(CHARACTERISTIC_UUID)
            print(f"Received: {response.decode()}")

            # # 클라이언트가 1분마다 실행되도록 조정
            # await asyncio.sleep(60)

    except Exception as e:
        print(f"Error during communication with the device: {e}")

if __name__ == "__main__":
    asyncio.run(run_client())
