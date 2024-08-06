import usb.core
import usb.util
import serial
import time
import serial.tools.list_ports


class SerialManager:
    def __init__(self, conf, logger):
        self.logger = logger
        self.conf = conf
        self.info = {
            "port": []
        }

    def init(self):
        self.info["port"] = []

    def find_usb_to_rs485(self, vendor_id, product_id):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vendor_id and port.pid == product_id:
                return port.device
        return None

    def findBySerialPort(self):
        self.init()
        self.logger.info("[SM] Find serial device by port ")
        vendor_id, product_id = self.conf['did'].split(':')
        # print(vendor_id, product_id)
        self.info["port"] = self.find_usb_to_rs485(
            int(vendor_id, 16), int(product_id, 16))
        # print(self.info["port"])

        if self.info["port"] != None:
            self.logger.info(
                f"[SM] USBtoRS485 Device Port:{self.info['port']}")
        else:
            self.logger.error("[SM] USBtoRS485 Device Not Found...")
        return self.info["port"]

    def write(self, port, req):
        serial_com = serial.Serial(
            port=port,
            baudrate=self.conf['baudrate'],
            bytesize=self.conf['bytesize'],
            parity=self.conf['parity'],
            stopbits=self.conf['stopbits'],
            timeout=2
        )

        try:
            self.logger.info("[SM] Read Data ...")
            serial_com.write(bytes(bytearray(req)))
            time.sleep(0.1)
            res = serial_com.readline()
            self.logger.info(f"[SM] Received Data : {res}")

            return res
        except Exception as e:
            self.logger.error(f"Error with : {e}")
            return
