FROM python:3.11-slim

# Working Directory 설정
WORKDIR /usr/src/app

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Dockerfile과 같은 경로의 모든 파일을 /usr/src/app으로 복사
COPY . .

# requirements.txt 내 라이브러리 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# SSL 인증서 복사
# COPY server.crt server.key ./

# logging Directory 추가
RUN mkdir -p /var/log/socketserver

# 83번 포트 오픈
EXPOSE 83

# 환경
ENV NAME SocketServer

# socketserver.py 실행
CMD ["python", "./socketserver.py"]