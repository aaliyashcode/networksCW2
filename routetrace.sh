#!/bin/bash
# Define an array with filenames as values
date
myArray=(www.washington.edu www.bijt.net www.ntua.gr www.harenet.ad.jp)
# Looping over for the two elements in myArray
for ((c=0; c<4; c++)); do
# For each iteration, printing out the value at that index [c]
echo ${myArray[${c}]}
traceroute -n ${myArray[${c}]}

done


