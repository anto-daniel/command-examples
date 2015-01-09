#!/bin/bash 

re='^[0-9]+$'
num=$1
if ! [[ $num =~ $re  ]]
then
    echo "Not a number"
    exit 1
fi

function recur  {

    number=$1
    digits=$(echo $number | egrep -o "[0-9]" | wc -l)
    if [[ $digits -gt 1 ]]
    then
        numsum=$(echo $number | egrep -o "[0-9]" | awk '{sum+=$1} END {print sum}')
        echo $numsum
        recur $numsum
    else
        echo "single digits asnwer $1"
    fi

}

recur $num 
