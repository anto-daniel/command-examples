#!/usr/bin/env python

from pymongo import MongoClient
import datetime, time
import sys
import ssl
import subprocess
import socket
import subprocess
import paramiko
import atexit

hostname = socket.gethostname()

#### For Mongo SSL Auth Connection ########
#mdb = MongoClient(hostname, 23758,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
#mdb.the_database.authenticate('admin', 'alcatraz1400', mechanism='SCRAM-SHA-1',source='admin')

### For Mongo Plain Connection #####
mdb = MongoClient(hostname, 27017)

#### Going to Mongo Database ####
db = mdb['alcatraz']
tenant = "prodnam"

class myssh:

    def __init__(self, host, user, password, port = 22):
        client = paramiko.SSHClient()
        #print "test"
        #client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=user, password=password)
        atexit.register(client.close)
        self.client = client

    def __call__(self, command):
        stdin,stdout,stderr = self.client.exec_command(command)
        sshdata = stdout.readlines()
        ssherr = stderr.readlines()
        retval = stdout.channel.recv_exit_status()
        return sshdata, ssherr, retval

def get_lag(group, topic, zkservers):
    kafka_bin = "/data1/kafka/kafka_2.9.1-0.8.1.1_actiance/bin"
    kafka_class = "kafka.tools.ConsumerOffsetChecker"
    cmd = kafka_bin+"/kafka-run-class.sh "+kafka_class+" --broker-info --group "+group+" --topic "+topic+" --zkconnect "+zkservers
    getlag_cmd = cmd+" | grep "+topic+" | awk '{sum+=$6} END {print sum}' "
    try:
        output = subprocess.check_output(getlag_cmd,shell=True,stderr=subprocess.STDOUT).rstrip()
        if "Exception" in output:
            print "group: "+group+" not found"
            output = group+" not found"
        if not output:
            print "topic not found"
            output = topic+": topic not found"
    except subprocess.CalledProcessError as e:
        output = "0"
        print "ERROR: ", e.output
    print output
    return output

def record_offsets(group, topic, zkservers):
    kafka_bin = "/opt/kafka/bin"
    kafka_class = "kafka.tools.ConsumerOffsetChecker"
    cmd = kafka_bin+"/kafka-run-class.sh "+kafka_class+" --broker-info --group "+group+" --topic "+topic+" --zkconnect "+zkservers
    getlag_cmd = cmd+" | grep "+topic+" | awk '{print $4}' | grep -E '[0-9]'"
    try:
        output = subprocess.check_output(getlag_cmd,shell=True,stderr=subprocess.STDOUT).rstrip()
        f = open('reindex_offsets', 'w')
        f.write(output)
        f.close()
        arr = output.split('\n')
        if "Exception" in output:
            print "group: "+group+" not found"
            output = group+" not found"
        if not output:
            print "topic not found"
            output = topic+": topic not found"
    except subprocess.CalledProcessError as e:
        output = "0"
        print "ERROR: ", e.output
    print arr
    return arr


def job_status(id1, collection):
    arr=[]
    lists = db.job_schedule.find({"_id":id1})
    print [arr.append(value["job_status"]) for value in lists]
    return arr[0]

jobs = db.job_schedule.find({"job_target" : "REINDEX", "trigger_type": "RECURRING"})
true_ids = []
for job in jobs:
    #print job
    id1 = job["_id"]
    if job["job_active_fl"]:
        print "Jobs which are true"
        print "id "+id1+": job_active_fl is "+str(job["job_active_fl"])
        true_ids.append(job["_id"])
        print "Updating "+id1+": job_active_fl to false"
        db.job_schedule.update({"_id": id1}, { '$set': {"job_active_fl": False}})
    else:
        print "id "+id1+": job_active_fl is "+str(job["job_active_fl"])

for id in true_ids:
    print id
    l = db.job_schedule.find({"_id":id})
    inst = l[0]
    status = inst["job_status"]
    while status != "COMPLETED":
        print  "job id:"+id+" is in "+status+" status"
        time.sleep(1)
        status = job_status(id,"job_schedule")
        print status

reindex_failed_msg = []
pdb = mdb[tenant]
pqry = pdb.reindex_failed_message.find({"status":"FAILED"})
pqry_refined = pdb.reindex_failed_message.find({"status":"FAILED"}, {"gcid":1, "event_audit_time":1,"_id":0})

for elem in pqry_refined:
    print elem
    reindex_failed_msg.append(elem)

for ele in reindex_failed_msg:
    print "reindex:reindex_failed_msg"
    ele["_id"] = ele["gcid"]
    del ele["gcid"]
    print ele
used = []
unique_docs = [x for x in reindex_failed_msg if x not in used and used.append(x)]

print "Printing uniq docs"
for ele in used:
    print ele


pqridx = pdb.reindex_gcid.delete_many({})
print "Cleared the data in collection reindex_gcid"
print str(pqridx.deleted_count)+" documents deleted in reindex_gcid"

result = pdb.reindex_gcid.insert([value for value in used])
print "New documents got inserted in reindex_gcid "
### To check new documents
#for doc in pdb.reindex_gcid.find():
#    print doc

offsets_check = record_lag("reindexConsumers","reIndex","fab-jpus01-zoo-h1:2471")
reindex_lag = get_lag("reindexConsumers","reIndex","fab-jpus01-zoo-h1:2471")
while reindex_lag == 0:
    print "Reindex lag still exists. Need to wait till the lag becomes zero"
    reindex_lag = get_lag("reindexconsumers","reindex","fab-jpus01-zoo-h1:2471")


host = "192.168.56.101"
try:
    remote1=myssh(host,"apcuser","facetime")
    try:
        karaf_cmd = 'apc-asm-reindex:reindex-custom -u apc_admin -p facetime -tenantId "'+tenant+'"'
        cmd = "/apps/karaf/bin/client "+karaf_cmd
        out1,err1,retval=remote1(cmd)
        print out1
        print err1
    except Exception as e:
        print "error", e
except socket.gaierror as e:
    print "\n"
    print "ERROR: Host "+host+" not reachable. Please provide proper hostname"
    sys.exit()

lfm =  db.job_schedule.find({}).sort("job_create_time",-1)

for doc in lfm:
    print doc
    id = doc["_id"]
    status = doc["job_status"]
    while status != "COMPLETED":
        print  "job id:"+id+" is in "+status+" status"
        time.sleep(1)
        status = job_status(id,"job_schedule")
        print status


#for id in true_ids:
#    print id
#    l = db.job_schedule.find({"_id":id})
#    inst = l[0]
#    status = inst["job_status"]
#    while status != "COMPLETED":
#        print  "job id:"+id+" is in "+status+" status"
#        time.sleep(1)
#        status = job_status(id,"job_schedule")
#        print status
#    print id+": setting it back to true"
#    db.job_schedule.update({"_id": id}, { '$set': {"job_active_fl": True}})
