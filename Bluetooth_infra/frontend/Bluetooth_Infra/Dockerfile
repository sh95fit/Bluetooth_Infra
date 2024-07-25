# 베이스 이미지 선정
FROM node:20.10.0-alpine AS build

# tzdata 설치
RUN apk add --no-cache tzdata

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . .

# 패키지 파일 복사 및 설치
COPY ./package.json ./package-lock.json ./

RUN npm install

# Vite 빌드
RUN npm run build

# 빌드 결과물을 /app/dist에 저장
CMD ["sh", "-c", "cp -r /app/dist/* /dist/ && tail -f /dev/null"]