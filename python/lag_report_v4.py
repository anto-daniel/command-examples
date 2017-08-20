#!/usr/bin/python

import urllib2, ssl
import sys, os, atexit
import json
import argparse
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import subprocess
import paramiko
import socket


parser = argparse.ArgumentParser()
parser.add_argument("--pr_host", help="enter the primary es hostname",required=True)
parser.add_argument("--pr_port", help="enter the primary es port",default=9640)
parser.add_argument("--dr_host", help="enter the dr es hostname",required=True)
parser.add_argument("--dr_port", help="enter the dr es port",default=9640)
parser.add_argument("--tenant", help="enter the tenant name",required=True)
parser.add_argument("--pr_user", help="enter the primary es username",default="admin")
parser.add_argument("--pr_pass", help="enter the primary es passwd",default="alcatraz1400")
parser.add_argument("--dr_user", help="enter the dr es username",default="admin")
parser.add_argument("--dr_pass", help="enter the dr es passwd",default="alcatraz1400")
parser.add_argument("--pr_ceph_host", help="enter the pr ceph host",default="fab-dr01-ceph-h1")
parser.add_argument("--dr_ceph_host", help="enter the dr ceph host",default="fab-dr02-ceph-h1")
#parser.add_argument("--kafzoo_hosts", help="enter the kafzoo hosts",required=True)
arg = parser.parse_args()
pr_es_host = arg.pr_host
pr_es_port = arg.pr_port.__str__()
dr_es_host = arg.dr_host
dr_es_port = arg.dr_port.__str__()
pr_es_user = arg.pr_user
pr_es_pass = arg.pr_pass
dr_es_user = arg.dr_user
dr_es_pass = arg.dr_pass
tenant_name = arg.tenant
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
today = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
primary_zkservers = "fab-dr01-kafzoo-h1:2471,fab-dr01-kafzoo-h2:2471,fab-dr01-kafzoo-h3:2471"
dr_zkservers = "fab-dr02-kafzoo-h1:2471,fab-dr02-kafzoo-h2:2471,fab-dr02-kafzoo-h3:2471"
pr_ceph_host = arg.pr_ceph_host
dr_ceph_host = arg.dr_ceph_host
user = "sysops"
password = "alcatraz1400"
cobj_pr_count = ""
fobj_pr_count = ""
lobj_pr_count = ""
cobj_dr_count = ""
fobj_dr_count = ""
lobj_dr_count = ""

SUBJECT = "PIPELINE LAG REPORT: VERSION 4: JPMC APAC"
#RECIPIENTS = "apaul@actiance.com,sappini@actiance.com,smohanty@actiance.com,hgangur@actiance.com"
RECIPIENTS = "apaul@actiance.com"
msg = MIMEMultipart()
msg['Subject'] = SUBJECT
msg['From'] = "no-reply@actiance.com"
msg['To'] = RECIPIENTS
msg.preamble = 'DR Env: DR END TO END INDEX LAG'
filename = "es_index_reports_"+today+"_"+tenant_name+"_v4.csv"
f = open(filename,"a")
pos = f.tell()

failed_shards = 0

if pos == 0:
        f.write("Time,Recv_Cnt,Ingest_Cnt,Ingest_Fail,Ingst_Q_PR,Ceph_Sync_Q_PR,LF_Q_PR,Ceph_Sync_Q_DR,LF_Q_DR,IDX_Q_DR,Ceph_OBJS_PR,Ceph_OBJS_DR,Ceph_OBJS_DIFF,Ceph_FILES_PR,Ceph_FILES_DR,Ceph_OBJS_DIFF,Ceph_LMSG_PR,Ceph_LMSG_DR,Ceph_LMSG_DIFF,SNAP_CNT_PR,SNAP_CNT_DR,SNAP_CNT_DIFF")
        f.write("\n")

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

def query_data(url, post):
    try:
        output = subprocess.check_output("./es_post_query.sh "+url+" '"+post+"'",shell=True)
    except subprocess.CalledProcessError as e:
        print e
    return output

def get_post_data(host,port,user,password,tenant,data):
    url = "https://"+host+":"+port+"/"+tenant+"_*/_search?pretty=true"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, user, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), handler)
    content = opener.open(url,data).read()
    jsond = json.loads(content)
    return jsond



def get_count(host,port,user,password,tenant):
        url = "https://"+host+":"+port+"/"+arg.tenant+"_*/idoc3/_count?pretty=true"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, user, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), handler)
        content = opener.open(url).read()
        jsond = json.loads(content)
        print "count of documents in "+tenant+":"+host+" = ", jsond["count"]
        count = jsond["count"]
        failed_shards = jsond["_shards"]["failed"]
#        print "->_shards->failed=>", failed_shards, type(failed_shards)
        if failed_shards != 0:
            time.sleep(10)
            content1 = opener.open(url).read()
            jsond1 = json.load(content1)
            failed_shards1 = jsond1["_shards"]["failed"]
            if failed_shards1 != 0:
                time.sleep(10)
                content2 = opener.open(url).read()
                jsond2 = json.load(content2)
                failed_shards2 = jsond2["_shards"]["failed"]
                if failed_shards2 != 0:
                    time.sleep(10)
                    content3 = opener.open(url).read()
                    jsond3 = json.load(content3)
                    failed_shards3 = jsond3["_shards"]["failed"]
                    failed_shards = failed_shards3
        return count


def get_lag(group, topic, zkservers):
    kafka_bin = "/opt/kafka/bin"
    kafka_class = "kafka.tools.ConsumerOffsetChecker"
    cmd = kafka_bin+"/kafka-run-class.sh "+kafka_class+" --broker-info --group "+group+" --topic "+topic+" --zkconnect "+zkservers
    getlag_cmd = cmd+" | grep "+topic+" | awk '{sum+=$6} END {print sum}' "
    try:
        output = subprocess.check_output(getlag_cmd,shell=True,stderr=subprocess.STDOUT).rstrip()
        if "Exception" in output:
            output = "0"
        if not output:
            output = "0"
    except subprocess.CalledProcessError as e:
        output = "0"
        print "ERROR: ", e.output
    print output
    return output

rs1_lag = get_lag("ingestionconsumers","rs1",primary_zkservers)
dr1_lag = get_lag("drPrimaryConsumer","drSeqPrimary",primary_zkservers)
dr2_lag = get_lag("drSecondayConsumer","drSeqSecondary",dr_zkservers)
index_lag = get_lag("reindexConsumers","reindex",dr_zkservers)
lfs_lag_pr = get_lag("ingestionlfsconsumers","lfs",primary_zkservers)
lfs_lag_dr = get_lag("ingestionlfsconsumers","lfs",dr_zkservers)


cnt1 = get_count(pr_es_host,pr_es_port,pr_es_user,pr_es_pass,tenant_name)
fd1 = failed_shards.__str__()
### 3 min delay between the quries ####
#time.sleep(180)
cnt2 = get_count(dr_es_host,dr_es_port,dr_es_user,dr_es_pass,tenant_name)


######### Getting Ceph DF COMMOBJECTS, FILES, LARGEMSG values #######
#host = "fab-dr01-ceph-h1"
#user = "sysops"
#password = "alcatraz1400"
try:
    remote1 = myssh(pr_ceph_host,user,password)
    remote2 = myssh(dr_ceph_host,user,password)
    try:
        cmd="echo "+password+" | sudo -S ceph df"
        out1,err1,retval=remote1(cmd)
        out2,err2,retval=remote2(cmd)
#    print out
        for i, j in enumerate(out1):
            if "COMMOBJECTS" in j:
                cobj = out1[i]
                cobj_arr = cobj.split()
                cobj_pr_count = cobj_arr[-1]
                print "COMMOBJECTS: PR: COUNT: ", cobj_pr_count
            elif "FILES" in j:
                fobj = out1[i]
                fobj_arr = fobj.split()
                fobj_pr_count = fobj_arr[-1]
                print "FILES: PR: COUNT: ", fobj_pr_count
            elif "LARGEMSG" in j:
                lobj = out1[i]
                lobj_arr = lobj.split()
                lobj_pr_count = lobj_arr[-1]
                print "LARGEMSG: PR: COUNT: ", lobj_pr_count

        for i, j in enumerate(out2):
            if "COMMOBJECTS" in j:
                cobj = out2[i]
                cobj_arr = cobj.split()
                cobj_dr_count = cobj_arr[-1]
                print "COMMOBJECTS: DR: COUNT: ", cobj_dr_count
            elif "FILES" in j:
                fobj = out2[i]
                fobj_arr = fobj.split()
                fobj_dr_count = fobj_arr[-1]
                print "FILES: DR: COUNT: ", fobj_dr_count
            elif "LARGEMSG" in j:
                lobj = out2[i]
                lobj_arr = lobj.split()
                lobj_dr_count = lobj_arr[-1]
                print "LARGEMSG: DR: COUNT: ", lobj_dr_count

    except Exception as e:
        print "error", e
except socket.gaierror as e:
    print "\n"
    print "ERROR: Ceph Host "+pr_ceph_host+" or "+dr_ceph_host+" not reachable. Please provide proper hostname" 
    sys.exit()


cobj_diff_int = int(cobj_pr_count) - int(cobj_dr_count)
cobj_diff = cobj_diff_int.__str__()
fobj_diff_int = int(fobj_pr_count) - int(fobj_dr_count)
fobj_diff = fobj_diff_int.__str__()
lobj_diff_int = int(lobj_pr_count) - int(lobj_dr_count)
lobj_diff = lobj_diff_int.__str__()


##### Received Count, Received Size ######
url1 = "https://"+pr_es_host+":"+pr_es_port+"/"+tenant_name+"_*/_search?pretty=true"
post1 = '{"_source": false,"aggs": {"types_count" : { "value_count" : { "field" : "processing_state" }},"total_native_size": {"sum": {"field": "native_size"}}}}'
post2 = '{"_source":false,"query":{"bool":{"must":[{"term":{"processing_state": "Archived"}}]}},"aggs":{"types_count":{"value_count":{ "field":"processing_state"}}}}'
post3 = '{"_source":false,"query":{"bool":{"must":[{"term":{"processing_state":"Failed"}}]}},"aggs":{"types_count":{"value_count":{"field":"processing_state"}}}}'

#output_query1 = query_data(url1, post1)
#output_query2 = query_data(url1, post2)
#output_query3 = query_data(url1, post3)
#jquery1 = json.loads(output_query1)
#jquery2 = json.loads(output_query2)
#jquery3 = json.loads(output_query3)
jquery1 = get_post_data(pr_es_host,pr_es_port,pr_es_user,pr_es_pass,tenant_name,post1)
jquery2 = get_post_data(pr_es_host,pr_es_port,pr_es_user,pr_es_pass,tenant_name,post2)
jquery3 = get_post_data(pr_es_host,pr_es_port,pr_es_user,pr_es_pass,tenant_name,post3)
received_count = jquery1["aggregations"]["types_count"]["value"]
received_size = jquery1["aggregations"]["total_native_size"]["value"]
ingested_count = jquery2["aggregations"]["types_count"]["value"]
failure_count = jquery3["aggregations"]["types_count"]["value"]
print "Received Size", received_size.__str__()
rc = received_count.__str__()
rs = received_size.__str__()
ic = ingested_count.__str__()
fc = failure_count.__str__()
print "Ingested Count", ic
print "Received Count", rc
print "Failure Count", fc

diff = cnt1 - cnt2
print "diff of primary and secondary counts of tenant "+arg.tenant+": ", diff.__str__()
#print type(st)
#print type(cnt1)
if failed_shards != 0:
    count1 = cnt1.__str__()+" ("+fd1+")"
else:
    count1 = cnt1.__str__()
count2 = cnt2.__str__()

diff_str = diff.__str__()
line = st+","+rc+","+ic+","+fc+","+rs1_lag+","+dr1_lag+","+lfs_lag_pr+","+dr2_lag+","+lfs_lag_dr+","+index_lag+","+cobj_pr_count+","+cobj_dr_count+","+cobj_diff+","+fobj_pr_count+","+fobj_dr_count+","+fobj_diff+","+lobj_pr_count+","+lobj_dr_count+","+lobj_diff+","+count1+","+count2+","+diff_str
print line
#f.write("TIMESTAMP,SNAPSHOT_COUNT_PRIMARY,SNAPSHOT_COUNT_SECONDARY,DIFF_OF_PRIMARY_SECONDARY")
#f.write("\n")
f.write(line)
f.write("\n")
f.close()
part = MIMEBase('application', "octet-stream")
part.set_payload(open(filename, "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')

msg.attach(part)

server = smtplib.SMTP("127.0.0.1")
server.sendmail("no-reply@actiance.com", RECIPIENTS.split(','), msg.as_string())
