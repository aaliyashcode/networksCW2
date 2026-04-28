#!/bin/bash
#Define an array with filenames as values
myArray=(www.washington.edu www.linkwan.com www.bijt.net www.ntua.gr) 
#loop
for ((c=0; c<4; c++)); do
# For each iteration, printing out the value at that index [c]
echo ${myArray[${c}]}
ping -c 120 ${myArray[${c}]}
done
