#!/bin/sh
fail2ban-server start
/usr/local/nginx/sbin/nginx -g "daemon off;" "$@"