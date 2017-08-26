#!/usr/bin/env python

from pymongo import MongoClient
import logging
import pymongo, ssl
import datetime, time


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


logging.info("Hello World!!!")
print "Hello"

def uniq_docs(seq, idfun=None):
    keys = {}
    for e in seq:
        print "INFO:FUNCTION:uniq_docs:elem:"+str(e)
        keys[str(e)] = 1
    return keys.keys()

reindex_failed_msg = []
pdb = mdb[tenant]
pqry = pdb.reindex_failed_message.find({"status":"FAILED"})
pqry_refined = pdb.reindex_failed_message.find({"status":"FAILED"}, {"gcid":1, "event_audit_time":1,"_id":0})

logging.info("Adding failed messages in array")

for elem in pqry_refined:
    print "appending:"+str(elem)
    reindex_failed_msg.append(elem)
