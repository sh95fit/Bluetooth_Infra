# 베이스 이미지로 Python 3.10 사용
FROM python:3.10

# 필요한 시스템 패키지 설치
RUN apt-get update && \
  apt-get install -y \
  bluez \
  libgirepository1.0-dev \
  libdbus-1-dev \
  build-essential \
  gcc \
  pkg-config \
  python3-dev \
  libglib2.0-dev \
  libcairo2-dev \
  python3-gi \
  python3-gi-cairo \
  python3-dbus \
  gir1.2-glib-2.0 \
  gir1.2-gdkpixbuf-2.0 \
  gir1.2-gtk-3.0 \
  gir1.2-pango-1.0 \
  && apt-get clean

# pip를 최신 버전으로 업그레이드
RUN pip install --upgrade pip setuptools

# PyGObject 패키지 설치
RUN pip install pycairo PyGObject

# pydbus 및 기타 Python 패키지 설치
RUN pip install pydbus
RUN pip install dbus-python

# 애플리케이션 파일 복사
WORKDIR /app
COPY . /app

# 실행 스크립트 설정
CMD ["python", "ble_server.py"]