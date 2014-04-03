from jira.client import JIRA 

options = {'server': 'https://jira.atlassian.com'}
jira = JIRA(options)

issue = jira.issue('JRA-9')
print issue.fields.project.key
print issue.fields.issuetype.name
print issue.fields.reporter.displayName

