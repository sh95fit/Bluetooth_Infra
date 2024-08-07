import os
import sys
import time
import datetime
import sched

from Utils.Logger import Logger
from Utils.TCP_Manager import TCP_Manager

from Configs.conf import Conf
from Inverter.Inverter import Inverter
from SerialManager import SerialManager


# VS 코드 실행 시 경로
logDirectory = './RaspberryPi_RTU/RTU_Master/logs'
# 명령 프롬프트 실행 시 경로
# logDirectory = './logs'

logger = Logger(logDirectory, 'a')

conf = Conf()
serial = SerialManager(conf.rs485, logger)
inverter = Inverter(conf.rs485, logger)

if hasattr(conf, "rs485"):
    device = Inverter(conf.rs485, logger)
    print(device)
else:
    logger.error("Device Not Found...")
    raise ValueError


# 통신 포트 불러오기
port = serial.findBySerialPort()

# 인버터 유형 지정
inverter_type = input("Inverter Type DIP >> ").strip()

# 인버터 목록 가져오기
ivt_list = inverter.getSerialNumber(inverter_type)


# 스케줄러 생성
scheduler = sched.scheduler(time.time, time.sleep)


def fetch_and_send_data():
    # 인버터 데이터 가져오기
    res = inverter.readData(inverter_type, port, ivt_list)

    if not res:
        print("Inverter Not Found...")
        return

    # 인버터 데이터 보내기
    for r in res:
        print(r)

        TCP_Manager(logger, r.hex())

        # 데이터 파서 적용 테스트
        # res = inverter.dataParser(inverter_type, r)
        # TCP_Manager(logger, res)


def schedule_task():
    # 1분마다 작업 실행
    scheduler.enter(60, 1, schedule_task)

    # 데이터 가져오고 보내기
    fetch_and_send_data()


# 초기 작업 스케줄링
schedule_task()

# 스케줄러 실행
scheduler.run()
