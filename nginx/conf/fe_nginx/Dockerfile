# nginx/Dockerfile
FROM nginx:1.23.2-alpine

# tzdata 설치
RUN apk add --no-cache tzdata

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 빌드된 React 파일 복사
VOLUME /usr/share/nginx/html

# Nginx 시작 명령
CMD ["nginx", "-g", "daemon off;"]