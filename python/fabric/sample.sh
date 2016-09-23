#!/bin/bash 

if [[ $1 == "" ]]
then
  echo "Please enter hostfilename in first arg"
  exit 1
fi

hosts=$1
for host in `cat hosts`
do
   echo $host
   #sshpass -p alcatraz1400 ssh -o StrictHostKeyChecking=no -o CheckHostIP=no -l sysops $host "echo alcatraz1400 | sudo -S sed -i \"/\/dev\/sdb1/ s/^/#/g\" /etc/fstab"
done
