#!/usr/bin/env python

from pymongo import MongoClient
import pymongo
import datetime, time
import sys
import ssl
import subprocess
import socket
import subprocess
import paramiko
import atexit
import json
import ast
### Hostname to run dr mongo and reindex queries
hostname = "fab-emdr01-karafui-h1-1"

#### For Mongo SSL Auth Connection ########
mdb = MongoClient(hostname, 23758,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
mdb.the_database.authenticate('admin', 'alcatraz1400', mechanism='SCRAM-SHA-1',source='admin')

### For Mongo Plain Connection #####
#mdb = MongoClient(hostname, 23758)

#### Going to Mongo Database ####
db = mdb['alcatraz']
tenant = "prodemea"

#### time

ts = time.time()
#st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
today = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%S')


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
    kafka_bin = "/opt/kafka/bin"
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
        reindex_offsets = "reindex_offsets_"+today+".txt"
        output = subprocess.check_output(getlag_cmd,shell=True,stderr=subprocess.STDOUT).rstrip()
        f = open(reindex_offsets, 'w')
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

def uniq_docs(seq, idfun=None):
    keys = {}
    for e in seq:
        print "INFO:FUNCTION:uniq_docs:elem:"+str(e)
        keys[str(e)] = 1
    return keys.keys()



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

print "INFO: waiting for the jobs to get COMPLETED"

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

print  "INFO: replacing gcid with _id"
for ele in reindex_failed_msg:
    print "reindex:reindex_failed_msg"
    ele["_id"] = ele["gcid"]
    print  "INFO: replacing gcid with _id "+ele["_id"]
    del ele["gcid"]
    ele["event_audit_time"] = str(ele["event_audit_time"])
    print ele

print "INFO: Making docs Uniq.."
used = uniq_docs(reindex_failed_msg)
print type(used)
print "INFO: Length of reindex_failed_message: "+str(len(reindex_failed_msg))
print "INFO: Length of array: "+str(len(used))
dups = len(reindex_failed_msg) - len(used)
print "INFO: Duplicates found: "+str(dups)
#unique_docs = [x for x in reindex_failed_msg if x not in used and used.append(x)]
print "INFO: Printing uniq docs"
for ele in used:
    print ele

print "Duplicates found: "+str(dups)

pqridx = pdb.reindex_gcid.delete_many({})
print "Cleared the data in collection reindex_gcid"
print str(pqridx.deleted_count)+" documents deleted in reindex_gcid"



for value in used:
    print "INFO: New document gonna insert: "+value
    jdump = json.dumps(value)
    jdict = json.loads(jdump)
    jeval = ast.literal_eval(jdict)
    print jeval['event_audit_time']
    try:
        result = pdb.reindex_gcid.insert_one({"_id":jeval['_id'],"event_audit_time":datetime.datetime.strptime(jeval['event_audit_time'],"%Y-%m-%d %H:%M:%S.%f")})
        print "INFO: New document "+value+" got inserted in reindex_gcid "
    except ValueError:
        try:
            result = pdb.reindex_gcid.insert_one({"_id":jeval['_id'],"event_audit_time":datetime.datetime.strptime(jeval['event_audit_time'],"%Y-%m-%d %H:%M:%S")})
            print "INFO: New document "+value+" got inserted in reindex_gcid "
        except pymongo.errors.DuplicateKeyError:
            print "ERROR: Skipping dup doc: "+value
    except pymongo.errors.DuplicateKeyError:
        print "ERROR: Skipping dup doc: "+value
#    print doc

reindex_lag = int(get_lag("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471"))
while reindex_lag != 0:
    print "reindex lag: "+str(reindex_lag)
    print "Reindex lag  still exists. Need to wait till the lag becomes zero"
    reindex_lag = int(get_lag("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471"))

offsets_check = record_offsets("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471")


host = "fab-emdr01-karafui-h1-1"
try:
    remote1=myssh(host,"sysops","alcatraz1400")
    try:
        karaf_cmd = 'apc-asm-reindex:reindex-custom -u apc_admin -p facetime -tenantId "'+tenant+'" -colName "reindex_gcid"'
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

reindex_lag1 = int(get_lag("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471"))
while reindex_lag1 != 0:
    print "reindex lag: "+str(reindex_lag1)
    print "Reindex lag  still exists. Need to wait till the lag becomes zero"
    reindex_lag1 = int(get_lag("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471"))

offsets_check1 = record_offsets("reindexConsumers","reindex","fab-emdr01-kafzoo-h1:2471")



#for id in true_ids:
#    print id+": setting it back to true"
#    db.job_schedule.update({"_id": id}, { '$set': {"job_active_fl": True}})
