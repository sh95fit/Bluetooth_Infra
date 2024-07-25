# Redis의 공식 Docker 이미지를 기반으로 합니다.
FROM redis:7.2.4-alpine3.19

COPY ./conf/redis.conf /usr/local/etc/redis/redis.conf

# Redis 서버를 실행
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

# Redis의 기본 포트인 6379 열기
EXPOSE 6379