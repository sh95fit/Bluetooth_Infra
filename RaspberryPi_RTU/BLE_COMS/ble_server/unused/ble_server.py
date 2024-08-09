# from pydbus import SystemBus
from dbus
from gi.repository import GLib
from dataclasses import dataclass

SERVICE_UUID = "19fa165e-dfe4-44ac-a518-1e71feae6900"
CHARACTERISTIC_UUID = "73c66424-9ace-492d-beb6-239ba04bdbf2"


@dataclass
class MyService:
    path: str
    uuid: str

    def __init__(self, path: str, uuid: str):
        self.path = path
        self.uuid = uuid

    def register(self, bus):
        # Get the GattManager1 interface to register the application

        # pydbus 활용 시
        # bluez = bus.get('org.bluez', '/org/bluez')
        # gatt_manager = bluez.get('org.bluez.GattManager1')
        # gatt_manager.RegisterApplication(self.path, {})

        # dbus 활용 시
        bus = dbus.SystemBus()
        bluez = bus.get_object('org.bluez', '/org/bluez')
        gatt_manager = dbus.Interface(bluez, 'org.bluez.GattManager1')
        gatt_manager.RegisterApplication(self.path, {})


@dataclass
class MyCharacteristic:
    path: str
    uuid: str
    value: bytes

    def __init__(self, path: str, uuid: str, value: bytes):
        self.path = path
        self.uuid = uuid
        self.value = value

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        self.value = value


class MyApplication:
    def __init__(self):
        self.bus = SystemBus()
        self.service = MyService('/myapp/service0', SERVICE_UUID)
        self.characteristic = MyCharacteristic(
            '/myapp/service0/char0', CHARACTERISTIC_UUID, b'Bluetooth Communication Success')
        self.service.register(self.bus)

    def run(self):
        loop = GLib.MainLoop()
        loop.run()


if __name__ == "__main__":
    app = MyApplication()
    app.run()
