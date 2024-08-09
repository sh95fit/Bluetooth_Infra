import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "19fa165e-dfe4-44ac-a518-1e71feae6900"
CHARACTERISTIC_UUID = "73c66424-9ace-492d-beb6-239ba04bdbf2"


async def scan_for_device_with_uuid(target_uuid):
    devices = await BleakScanner.discover()
    for device in devices:
        # Attempt to find the service UUID in the advertised services
        if target_uuid in device.metadata.get("uuids", []):
            return device.address
    return None


async def connect_and_interact(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        # Write data to characteristic
        new_value = b'Hello from Windows'
        await client.write_gatt_char(CHARACTERISTIC_UUID, new_value)
        print(f"Written value: {new_value}")

        # Read data from characteristic
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print(f"Characteristic Value: {value.decode('utf-8')}")


async def main():
    print("Scanning for devices...")
    device_address = await scan_for_device_with_uuid(SERVICE_UUID)

    if device_address:
        print(f"Found device with UUID {SERVICE_UUID}: {device_address}")
        await connect_and_interact(device_address)
    else:
        print(f"No device found with UUID {SERVICE_UUID}")

if __name__ == "__main__":
    asyncio.run(main())
