#!/bin/bash

URL="https://mirror.tngnet.com/speedtests/100MB.bin"

for ((kk=1; kk<=5; k++))
do

echo  "kk = $kk"
  for ((ii=1; ii<=kk; i++))
  do
     wget -O /dev/null "$URL" 2>&1
  done

  wait
done

for ((k=1; k<=5; k++))
do

echo  "k = $k"
  for ((i=1; i<=k; i++))
  do
     wget -O /dev/null "$URL" 2>&1 | grep "MB/s"
  done

  wait

done