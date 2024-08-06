from Utils.CRC16 import crc16
import os
import sys
import time
import serial

sys.path.append(os.path.dirname(os.path.abspath(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


class ESP_25K:
    confSets = {
        "rs485": {
            "did": "0403:6001",
            "baudrate": 9600,
            "bytesize": serial.EIGHTBITS,
            "parity": serial.PARITY_NONE,
            "stopbits": serial.STOPBITS_ONE
        },
        "triple": {
            "write": {
                "size": 8,
                "function": 0x03,
                "start_high": 0x75,
                "start_low": 0x61,
                "register_high": 0x00,
                "register_low": 0x1b
            }
        }
    }

    def makeRequestData(self, id):
        req = [0xFF & id,
               self.confSets["triple"]["write"]["function"],
               self.confSets["triple"]["write"]["start_high"],
               self.confSets["triple"]["write"]["start_low"],
               self.confSets["triple"]["write"]["register_high"],
               self.confSets["triple"]["write"]["register_low"]]
        req.extend(crc16(req))
        return req
