from pydbus import SystemBus
from gi.repository import GLib
import time

SERVICE_UUID = "19fa165e-dfe4-44ac-a518-1e71feae6900"
CHARACTERISTIC_UUID = "73c66424-9ace-492d-beb6-239ba04bdbf2"


def scan_for_device(target_uuid):
    bus = SystemBus()
    adapter = bus.get('org.bluez', '/org/bluez/hci0')

    # Start scanning
    adapter.StartDiscovery()
    print("Scanning for devices...")

    # Give it some time to discover devices
    time.sleep(10)

    # Stop scanning
    adapter.StopDiscovery()
    print("Stopped scanning.")

    # Get discovered devices
    manager = bus.get('org.bluez', '/org/bluez')
    for device_path in manager.Adapter1.GetManagedObjects():
        device = bus.get('org.bluez', device_path)
        advertised_uuids = device.UUIDs
        if target_uuid in advertised_uuids:
            return device_path

    return None


def main():
    target_uuid = SERVICE_UUID
    device_path = scan_for_device(target_uuid)

    if device_path:
        print(f"Found device with UUID {target_uuid}: {device_path}")
        device = SystemBus().get('org.bluez', device_path)
        # Here you can interact with the device, read/write characteristics
        char = device.findCharacteristic(
            CHARACTERISTIC_UUID)
        if char:
            value = char.ReadValue({})
            print("Characteristic Value: ", value.decode('utf-8'))
    else:
        print(f"No device found with UUID {target_uuid}")


if __name__ == "__main__":
    main()
