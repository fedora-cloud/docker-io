#!/bin/sh

for id in $(docker ps -q); do
    docker exec $id logrotate -s /var/log/logstatus /etc/logrotate.conf > /dev/null 2>&1
done
exit 0
