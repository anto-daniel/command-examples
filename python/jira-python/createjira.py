import sys, getopt
from jira.client import JIRA

options = {'server':'https://jira.corp.inmobi.com', 'verify':False}
jira = JIRA(options, basic_auth=('anto.daniel','xxxxxx'))

proj = raw_input("Enter ProjectType: ")
print proj
summary = raw_input("Enter Summary: ")
print summary
desc = raw_input("Enter Description: ")
print desc

#summary = sys.argv[1]

issue = jira.create_issue(project={'key': ""+proj+""}, summary=""+summary+"",description=""+desc+"",issuetype={'name': 'Bug'},assignee={'name': 'anto.daniel','emailAddress': 'anto.daniel@inmobi.com'})
print issue
#user_created = issue.fields.creator
#description = issue.fields.description.title()
#print "Ticket Created by: "+user_created.__str__()+"\n"
#print "Ticket Description: "+description+"\n"
#print "Comments: "
#for comment in issue.fields.comment.comments:
#    print comment.id
#    print comment.body
 
