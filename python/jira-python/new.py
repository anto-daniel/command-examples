from jira.client import JIRA 

options = {'server': 'https://jira.atlassian.com','headers':''}
#jira = JIRA(options)
jira = JIRA(options, basic_auth=('anto.daniel','1ds01is005'), oauth=None, validate=None)
#jira = JIRA(options = jira_options, basic_auth = ('anto.daniel@gmail.com','1ds01is005'))
#projects = jira.projects()
#keys = sorted([project.key for project in projects])[2:5]
#issue = jira.issue('TST-53430')
#import re
#atl_comments = [comment for comment in issue.fields.comment.comments
#                                if re.search(r'@atlassian.com$', comment.author.emailAddress)]
#for comment in issue.fields.comment.description:
#    print comment
#print issue.fields.comments.comment

props = jira.search_issues('reporter=anto.daniel')

