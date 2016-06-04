#!/bin/bash 

count=1
for i in "$*"
do
    echo "\$* Parameter #$count = $i"
    count=$[ $count + 1 ]
done


count=1
for i in "$@"
do
    echo "\$@ Parameter #$count = $i"
    count=$[ $count + 1 ]
done

