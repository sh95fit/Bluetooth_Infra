FROM python:3.9-slim

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Celery Worker에서 사용된 패키지 설치를 위해 celery_task의 requirements.txt 패키지 복사
COPY ./requirements.txt .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["celery", "-A", "beat.celery_beat", "worker", "--loglevel=info"]