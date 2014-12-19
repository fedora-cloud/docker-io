#!/bin/sh

LOGROTATE=true
[ -f /etc/sysconfig/docker ] && source /etc/sysconfig/docker

if [ $LOGROTATE == true ]; then
    for id in $(docker ps -q); do
        exec $(docker exec $id logrotate -s /var/log/logstatus /etc/logrotate.conf > /dev/null 2&>1)
    done
fi
exit 0
