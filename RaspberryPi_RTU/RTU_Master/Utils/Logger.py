import os
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler

# ANSI Escape codes prefix

# 모든 색상 및 스타일 초기화
RESET_SEQ = "\033[0m"
# 텍스트 색상 변경 (%d에 색상 코드 반영)
COLOR_SEQ = "\033[1;%dm"
# 텍스트에 굵은 스타일 적용
BOLD_SEQ = "\033[1m"


# 텍스트 색상 코드
# ex> Black: "\033[30m", Red: "\033[31m", Green: "\033[32m", Yello: "\033[33m", Blue: "\033[34m", Magenta: "\033[35m", Cyan: "\033[36m", White: "\033[37m"

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': MAGENTA
}


# Changing prefix to Escape code
def form(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


# logging.Formatter 객체 상속
# format 함수를 오버라이딩하여 재정의
class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        # logging.Formatter 클래스의 생성자를 호출하여 객체를 초기화
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    # record는 로그 레코드 객체로 asctime, levelname, message, filename, lineno, funcName, name, process, thread 등의 속성을 포함하고 있음
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def Logger(path, mode='a'):
    # 포멧 정의
    # File format, [UTC TIME][LEVELS] MSG (Filename:Line)
    # asctime : LogRecord가 생성된 시간
    # levelname : 메세지 텍스트 로깅 수준 ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    # message : 로그 된 메세지(Formatter.format()이 호출될 때 설정)  < msg % args로 계산
    # filename : pathname의 파일명 부분
    # lineno : 로깅 호출이 일어난 소스 행 번호
    FILE_FORMAT = form(
        "[%(asctime)s][%(levelname)-8s] %(message)s (%(filename)s:%(lineno)d)", False)
    file_format = ColoredFormatter(FILE_FORMAT, False)

    # Console format, [UTC TIME][LEVELS] MSG
    CONSOLE_FORMAT = form("[%(asctime)s][%(levelname)-18s] %(message)s", True)
    console_format = ColoredFormatter(CONSOLE_FORMAT)

    # Logger 정의
    fileHandler = TimedRotatingFileHandler(
        path+"/RTU.log", when="midnight", interval=1)
    # 새로운 파일 생성 시 날짜 추가
    fileHandler.suffic = "%Y%m%d"
    # 포멧 지정
    fileHandler.setFormatter(file_format)

    # 로그 정보가 출력되는 위치 설정 (default : sys.stderr)
    # 표준 출력으로 변경 (sys.stdout)
    streamHandler = logging.StreamHandler(stream=sys.stdout)
    # 포멧 지정
    streamHandler.setFormatter(console_format)

    # 로거 생성 (logging.getLogger() 또는 logging.getLogger("")은 루트 로거를 생성 (기본 레벨 warning))
    logger = logging.getLogger('RTU')
    # 특정 레벨 이상의 log만 출력하도록 설정
    logger.setLevel(logging.DEBUG)
    # 핸들러 추가 (fileHandler, streamHandler)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger
