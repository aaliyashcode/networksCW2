#!/bin/bash 
# Define an array with filenames as values 

echo "# timeuk=$(date +"%Y-%m-%d %H:%M:%S")" 
myURL=(https://mirror.vpgrp.io/debian/dists/Debian12.13/contrib/dep11/icons-64x64.tar.gz https://mirror.tngnet.com/linux/ubuntureleases/14.04.6/ubuntu-14.04.6-desktop-amd64.iso.zsync https://mirror.tngnet.com/speedtests/100MB.bin )

for ((c=0; c<3; c++)); do 
for ((b=1; b<=10; b++)); do
echo ${myURL[${c}]} 
wget -O /dev/null ${myURL[${c}]} 2>&1
done 
done
