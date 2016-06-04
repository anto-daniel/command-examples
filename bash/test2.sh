#!/bin/bash 

trap "echo 'bye bye'" EXIT

count=1
while [ $count -le 10 ]
do
    echo "Loop #$count"
    sleep 3
    count=$[ $count + 1 ]
done

trap - EXIT
echo "I just removed the trap"
