import serial


class Conf:
    rs485 = {
        "did": "0403:6001",
        "baudrate": 9600,
        "bytesize": serial.EIGHTBITS,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE
    }
