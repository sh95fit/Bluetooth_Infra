FROM python:alpine

# 최신 루트 인증서와 시간대 정보를 업데이트
RUN apk add --no-cache ca-certificates tzdata && update-ca-certificates

# Celery Worker에서 사용된 패키지 설치를 위해 celery_task의 requirements.txt 패키지 복사
COPY ./requirements.txt .

RUN pip install --no-cache-dir redis flower celery
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# PYTHONUNBUFFERED: Python 표준 입출력이 버퍼링 되지 않도록 설정
# PYTHONHASHSEED: 해시 랜덤화 (Python은 해시 값의 일관성을 보장하지 않으므로 실행 시마다 해시값이 다르게 생성되도록 한다 (해시 충돌 공격에 대한 저항력을 높이는 목적))
# PYTHONDONTWRITEBYTECODE: (.pyc 바이트 코드 파일을 디스크에 쓰지 않도록 설정 / 일반적으로 .py 파일의 바이트 코드 버전인 .pyc를 저장하나 1로 설정하면 생성되지 않음 / 읽기 전용)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

# Default port
EXPOSE 5555

# 도커 볼륨으로 지정해서 지속적으로 저장하기 위한 경로
ENV FLOWER_DATA_DIR /data
# 파이썬이 모듈을 찾을 때 참조하는 경로
ENV PYTHONPATH /app

WORKDIR $FLOWER_DATA_DIR

# flower:flower에 속하는 flower 계정 생성
RUN set -eux; \
  addgroup -g 1000 flower; \
  adduser -u 1000 -G flower flower -D; \
  mkdir -p "$FLOWER_DATA_DIR"; \
  chown flower:flower "$FLOWER_DATA_DIR"
USER flower

VOLUME $FLOWER_DATA_DIR

CMD ["celery", "flower", "--broker=${CELERY_FLOWER_BROKER_URL}"]