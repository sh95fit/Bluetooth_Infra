FROM python:3.11-slim

WORKDIR /src

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["celery", "-A", "tasks.save_to_mysql", "worker", "--loglevel=info"]