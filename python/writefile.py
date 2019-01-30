#!/usr/bin/env python

import sys
import re
import datetime
import random


CURDATE = datetime.datetime.now()
REQDATE = re.sub(r'(.*)\..*',r'\1',str(CURDATE)) 
num1 = random.randint(1,100)
num2 = random.randint(1,10)
num3 = random.randint(1,90)
num4 = random.randint(1,10)
num5 = random.randint(100,999)
f = open("/home/user/karaf.log","a")
f.write(REQDATE+","+str(num5)+"  | INFO  | Thread-97        | AlcatrazStats                    | 178 - actiance-commons-utils - 1.0.0.g82f30d8 | IngestInteraction\n")
f.write("\t\tIngestionRate count=0, totaltime=0, avg=0, min=0, max=0, at=None\n")
f.write("\t\tKafka-ingest-time count=0, totaltime=0, avg=0, min=0, max=0, at=None\n")
f.write("\t\tKafka-success total=0 rate=0/sec\n")
f.write("\t\tsuccess total="+str(num1)+" rate="+str(num2)+"/sec \n")
f.write("\t\tfailure total="+str(num3)+" rate="+str(num4)+"/sec \n")
f.close()
