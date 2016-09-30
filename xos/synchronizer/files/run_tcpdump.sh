#! /bin/bash
INTERFACE=$1
tcpdump -n -e -i $INTERFACE -c 10 &
curl http://xosproject.org/ &> /dev/null &
sleep 10s
