FROM alpine:3.16.3

RUN apk update && apk upgrade
RUN apk add --update wget \
  tar \
  autoconf \
  automake \
  build-base \
  git \
  openssl-dev \
  curl-dev \
  geoip-dev \
  lmdb-dev \
  pcre-dev \
  libtool \
  libxml2-dev \
  libressl-dev \
  yajl-dev \
  pkgconf  \
  zlib-dev \
  linux-headers

# tzdata 설치
RUN apk add --no-cache tzdata

# 시간대 설정 (예: Asia/Seoul)
ENV TZ=Asia/Seoul
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN cd /tmp && git clone https://github.com/SpiderLabs/ModSecurity
RUN cd /tmp/ModSecurity && git submodule init && git submodule update
RUN cd /tmp/ModSecurity && ./build.sh && \
  ./configure && \
  make && \
  make install

RUN cd /tmp && git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git \
  && wget http://nginx.org/download/nginx-1.23.2.tar.gz \
  && tar zxvf nginx-1.23.2.tar.gz

RUN cd /tmp/nginx-1.23.2/ && ./configure  --user=root --group=root --with-debug --with-ipv6	--with-http_ssl_module --with-compat --add-module=/tmp/ModSecurity-nginx --with-http_stub_status_module --without-http_access_module --without-http_auth_basic_module --without-http_autoindex_module --without-http_empty_gif_module --without-http_fastcgi_module --without-http_referer_module --without-http_memcached_module --without-http_scgi_module --without-http_split_clients_module --without-http_ssi_module --without-http_uwsgi_module \
  && make \
  && make install

RUN git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git /usr/src/owasp-modsecurity-crs
RUN cp -R /usr/src/owasp-modsecurity-crs/rules/ /usr/local/nginx/conf/
RUN mv /usr/local/nginx/conf/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example  /usr/local/nginx/conf/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
RUN mv /usr/local/nginx/conf/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example  /usr/local/nginx/conf/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

RUN apk add fail2ban
RUN rm /etc/fail2ban/jail.d/alpine-ssh.conf

EXPOSE 80

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]