#!/bin/bash


### Enter erb file in 1st arg
erb=$1
if ! [[ $erb =~ ".erb" ]]
then
    echo "Please enter erb file in 1st argument..."
    exit 1
fi
prop=$2

if ! [[ $prop =~ ".properties" ]]
then
    echo "Please enter server properties file in 2nd argument .."
    exit 1
fi
cp $prop final.erb
egrep "=" $prop | awk -F= '{print $1}' > lhs

#cat lhs

#echo -e "\n\n\n\n"

cat lhs | while read -r line 
do 
    cmd=$(grep $line $erb | grep '<%=')
    if [ $? -eq 0 ]
    then
        rline=$(grep $line $erb)
        if [ $? -eq 0 ]
        then
            sed -i "/$line/c ${rline}" final.erb 2>error
        fi
    fi
done 

sed -i 's///g' final.erb
