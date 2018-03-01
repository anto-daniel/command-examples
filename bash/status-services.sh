#!/bin/bash

user=$(whoami)
RED=`tput setaf 1`
GREEN=`tput setaf 2`
NC=`tput sgr0`
if [[ $user != "root" ]]; then
    echo "Please execute this script as root, not as user $user. Exiting!!!"
    exit 1
fi


for i in ceph-mon@fab-alcz-sandbox-h2 ceph-osd.target ceph-radosgw.target mongod elasticsearch stormnimbus stormsupervisor stormui karaf karaf-nfs hazelcast zookeeper kafka
do
    status=$(systemctl is-active $i)
    if [[ $status != "active" ]]; then
        echo "${RED}RED${NC}: Fabric: $i: Not Running"
    else
        echo "${GREEN}GREEN${NC}: Fabric: $i: Running"
    fi
done
