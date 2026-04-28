#!/bin/bash

URL="https://mirror.tngnet.com/speedtests/100MB.bin"
Message="Normal Ping"
Message2="While large file transfer"

echo $Message
ping -c 10 mirror.tngnet.com

echo $Message2

for ((k=1; k<=5; k++))
    do
	ping -c 5 mirror.tngnet.com &
	wget -O /dev/null "$URL" 2>&1 | grep "MB/s" &

  wait

done

