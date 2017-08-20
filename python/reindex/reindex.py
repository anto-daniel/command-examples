#!/usr/bin/env python

from pymongo import MongoClient
import datetime
import sys
import ssl
import subprocess
import socket

hostname = socket.gethostname()

#### For Mongo SSL Auth Connection ########
#mdb = MongoClient(hostname, 23758,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
#mdb.the_database.authenticate('admin', 'alcatraz1400', mechanism='SCRAM-SHA-1',source='admin')

### For Mongo Plain Connection #####
mdb = MongoClient(hostname, 27017)

#### Going to Mongo Database ####
db = mdb['alcatraz']



jobs = db.job_schedule.find({"job_target" : "REINDEX", "trigger_type": "RECURRING"})
true_ids = []
for job in jobs:
    #print job
    id1 = job["_id"]
    if job["job_active_fl"] != "false":
        print "Jobs which are true"
        print "id "+id1+": job_active_fl is "+job["job_active_fl"]
        true_ids.append(job["_id"])
        print "Updating "+id1+": job_active_fl to false"
        db.job_schedule.update({"_id": id1}, { '$set': {"job_active_fl": "false"}})
    else:
        print "id "+id1+": job_active_fl is "+job["job_active_fl"]



for id in true_ids:
    print id
    l = db.job_schedule.find({"_id":id})
    print l
