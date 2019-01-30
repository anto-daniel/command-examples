#!/bin/bash

hostfile=${1}
commands_list=${2}
user=user
pass=xxxx
if [[ $hostfile == "" || $commands_list == "" ]]
then
    echo "Usage: ./run_cmd.sh <host list file> <commands list file>"
    exit 1
fi

for host in `cat $hostfile`
do
        echo -n "$host\n"
        all_cmd=$(cat $commands_list | sed ':a;N;$!ba;s/\n/\ \&\&\ /g')
        sshpass -p $pass ssh -t -t -o StrictHostKeyChecking=no $user@$host  "$all_cmd"
done
