from bluepy3.btle import Peripheral, UUID, Service, Characteristic
import time

SERVICE_UUID = UUID("19fa165e-dfe4-44ac-a518-1e71feae6900")
CHARACTERISTIC_UUID = UUID("73c66424-9ace-492d-beb6-239ba04bdbf2")


class MyCharacteristic(Characteristic):
    def __init__(self, service):
        Characteristic.__init__(self, CHARACTERISTIC_UUID,
                                Characteristic.PROP_READ | Characteristic.PROP_WRITE,
                                Characteristic.PERM_READ | Characteristic.PERM_WRITE, service)
        self.value = b"Send from BLE Server"

    def read(self):
        return self.value

    def write(self, value):
        self.value = value


class MyService(Service):
    def __init__(self):
        Service.__init__(self, SERVICE_UUID)
        self.char = MyCharacteristic(self)


if __name__ == "__main__":
    peripheral = Peripheral()
    peripheral.addService(MyService())

    print("Peripheral started. Waiting for connection...")
    try:
        while True:
            time.sleep(1)  # 계속 실행되도록 대기
    except KeyboardInterrupt:
        peripheral.disconnect()
        print("Peripheral stopped.")
