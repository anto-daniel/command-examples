import sys, getopt
from jira.client import JIRA

options = {'server':'https://jira.corp.domain.com','verify':False}
jira = JIRA(options, basic_auth=('anto.daniel','xxxxxxxxx'))

ticketid = sys.argv[1]
#addcomment = sys.argv[2]
issue = jira.issue(ticketid)
transitions = jira.transitions(issue)
[(t['id'], t['name']) for t in transitions]
for t in transitions:
    print t['id'], t['name']
#print transitions
#jira.transition_issue(issue,'2', assignee={'name':'anto.daniel'}, resolution={'id': '1' }, rca={'id':'2'})
jira.transition_issue(issue,'2', assignee={'name':'anto.daniel'})
print issue.__str__()+" Closed."
