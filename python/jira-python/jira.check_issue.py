#!/usr/bin/env python

import sys, getopt
from jira.client import JIRA

options = {'server':'https://jira.corp.domain.com', 'verify':False}
jira = JIRA(options, basic_auth=('anto.daniel','xxxxxxxx'))

ticketid = sys.argv[1]
issue = jira.issue(ticketid)
user_created = issue.fields.creator
description = issue.fields.description.title()
print "Ticket Created by: "+user_created.__str__()+"\n"
if description is None:
    print "No Description written"
else:
    print "Ticket Description: "+description+"\n"
print "Comments: "
for comment in issue.fields.comment.comments:
    print comment.id
    print comment.body
    
