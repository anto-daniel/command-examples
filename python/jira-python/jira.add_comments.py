import sys, getopt
from jira.client import JIRA

options = {'server':'https://jira.corp.inmobi.com','verify':False}
jira = JIRA(options, basic_auth=('anto.daniel','xxxxxxxx'))

ticketid = sys.argv[1]
addcomment = sys.argv[2]
comment = jira.add_comment(ticketid, addcomment)
print 'added comment'
