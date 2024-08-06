from Inverter.DongYang import ESP25K
from SerialManager import SerialManager


class Inverter:
    def __init__(self, conf=None, logger=None):
        self.logger = logger
        self.conf = conf
        self.serial = SerialManager(self.conf, self.logger)
        self.inverter = {
            "dip1": ESP25K.ESP_25K
        }

    def getSerialNumber(self, dip):
        self.dip = dip

        self.ivt = self.inverter[self.dip]()
        ivt_list = []

        self.logger.info("[IVT] Find Serial Number ...")
        try:
            port = self.serial.findBySerialPort()
            for i in range(100):
                req = self.ivt.makeRequestData(i)

                # To Do
                # SerialManager Write 완성 및 데이터 없음(Null)이 아닐 경우 국번 추가
                if self.serial.write(port, req):
                    ivt_list.append(i)
                else:
                    pass

            self.logger.info(f"[IVT] Valied Inverter : {ivt_list}")
            return ivt_list

        except KeyboardInterrupt as e:
            self.logger.info(f"[IVT] Force Quit... {e}")
            return ivt_list

    def readData(self, dip, port, ivt_list):
        res_list = []
        for ivt in ivt_list:
            self.logger.info(f"[IVT] Read Inverter {ivt} Data ...")
            req = self.ivt.makeRequestData(ivt)

            res = self.serial.write(port, req)
            res = bytes([ivt])+res
            print(res.hex())
            print(len(res.hex()), len(res))

            if res:
                res_list.append(res)

        return res_list
