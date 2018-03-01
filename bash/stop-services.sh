#!/bin/bash


systemctl stop karaf-nfs
systemctl stop karaf
systemctl stop stormsupervisor
systemctl stop stormui
systemctl stop stormnimbus
systemctl stop hazelcast
systemctl stop kafka
systemctl stop zookeeper
systemctl stop elasticsearch
systemctl stop mongod
systemctl stop ceph-radosgw.target
systemctl stop ceph-osd.target
systemctl stop ceph-mon.target
