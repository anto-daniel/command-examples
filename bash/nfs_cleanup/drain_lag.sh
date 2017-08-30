#!/bin/bash

kafka_dir='/logs/nfs_scripts/kafka_2.11-0.11.0.0'
kafka_bin_dir="$kafka_dir/bin"
kafka_class='kafka.tools.ConsumerOffsetChecker'
group=$1
topic=$2
zkservers_port=$3

if [[ $group == "" || $topic == "" || $zkservers_port == "" ]]
then
   echo -e "Usage: $0 <group> <topic> <zkserver1:port,zkserver2:port,...>"
   exit 1
fi

/bin/bash $kafka_bin_dir/kafka-run-class.sh $kafka_class --topic $topic --group $group --zookeeper $zkservers_port | grep -vE "^Group|BROKER|->" > van01_stats.txt
cat van01_stats.txt | awk '{print $5}' > van01_logsize.txt
/bin/bash $kafka_bin_dir/kafka-run-class.sh $kafka_class --topic $topic  --group $group   --zookeeper $zkservers_port | grep -vE "^Group|BROKER|->" | awk '{print $4}' > van01_offsets.txt
first_logsize=$(cat van01_logsize.txt | head -1)
curr_offset=$(cat van01_offsets.txt | head -1)
paste van01_offsets.txt van01_logsize.txt > curr_stats.txt
cat curr_stats.txt | awk '{print $1-$2}' > stats.txt
paste curr_stats.txt stats.txt > stat.txt
#echo -e "\nCurrent Offset\t| Initial Logsize\t| Diff"
#cat stat.txt

while [[ $(egrep '-' stat.txt) ]]
do
   rm -rf van01_offsets.txt stats.txt stat.txt
   /bin/bash $kafka_bin_dir/kafka-run-class.sh $kafka_class --topic $topic  --group $group   --zookeeper $zkservers_port | grep -vE "^Group|BROKER|->" | awk '{print $4}' > van01_offsets.txt
   curr_offset=$(cat van01_offsets.txt | head -1)
   paste van01_offsets.txt van01_logsize.txt > curr_stats.txt
   cat curr_stats.txt | awk '{print $1-$2}' > stats.txt
   paste curr_stats.txt stats.txt > stat.txt
   echo -ne "Sleep for 10 seconds. Still $(cat stat.txt| awk '{sum+=$3} END {print sum}'|sed 's/\-//g') messages are draining ...\r"
   sleep 10
#   echo -e "\nCurrent Offset\t| Initial Logsize\t| Diff"
#   cat stat.txt
#   echo -e "\n\n"
done
