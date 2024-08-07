from Utils.CRC16 import crc16
import os
import sys
import time
import serial
from datetime import datetime
import json

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

    def dataParser(self, req):
        req = req.hex()
        try:
            if len(req) == 120:
                data = {
                    "device_id": int(req[0:2], 16),
                    "outar": int(req[8:12], 16)/10,
                    "outas": int(req[12:16], 16)/10,
                    "outat": int(req[16:20], 16)/10,
                    "outvrs": int(req[20:24], 16),
                    "outvst": int(req[24:28], 16),
                    "outvtr": int(req[28:32], 16),
                    "tpg": int(req[32:40], 16)/100,
                    "operation": int(req[40:44], 16),
                    "message": int(req[44:52], 16),
                    "cpg": int(req[52:60], 16),
                    "ina1": int(req[60:64], 16)/10,
                    "inv1": int(req[64:68], 16),
                    "ina2": int(req[68:72], 16)/10,
                    "inv2": int(req[72:76], 16),
                    "ina3": int(req[76:80], 16)/10,
                    "inv3": int(req[80:84], 16),
                    "ina4": int(req[84:88], 16)/10,
                    "inv4": int(req[88:92], 16),
                    "ina5": int(req[92:96], 16)/10,
                    "inv5": int(req[96:100], 16),
                    "ina6": int(req[100:104], 16)/10,
                    "inv6": int(req[104:108], 16),
                    "temp": int(req[108:112], 16),
                    "fr": int(req[112:116], 16),
                    "savetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

            if data:
                json_data = json.dumps(data)
                encode_json_data = json_data.encode('utf-8')
                print(len(encode_json_data), encode_json_data)

                return encode_json_data
            else:
                print("[ESP25K] Data Length Incorrect...")
                return
        except Exception as e:
            print(f"Error with : {e}")
            return
