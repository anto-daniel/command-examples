#!/usr/bin/env python
""" This Script helps in creating InMobi JIRA ticket """

import sys
import getopt
from jira.client import JIRA
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--project",help="Project Type")
parser.add_argument("--summary",help="Summary")
parser.add_argument("--description",help="Description")
args = parser.parse_args()

<<<<<<< HEAD

class CreateJIRA:
    """ Main Class """

    def __init__(self):
        """ Initial Variables """

        self.emailid = "anto.daniel@inmobi.com"
        options = {'server': 'https://jira.corp.inmobi.com', 'verify': False}
        self.jira = JIRA(options, basic_auth=('anto.daniel', 'Rachel@123'))

    def enter_details(self):
        """ Enter Details to create JIRA """

        self.proj = raw_input("Enter ProjectType: ")
        print self.proj
        self.summary = raw_input("Enter Summary: ")
        print self.summary
        self.desc = raw_input("Enter Description: ")
        print self.desc
        

    def create_jira(self):
        """ With previous method details, creats jira ticket """

        issue = self.jira.create_issue(project={'key': ""+self.proj+""},
                                       summary=""+self.summary+"",
                                       description=""+self.desc+"",
                                       assignee={'name': 'anto.daniel',
                                                 'emailAddress': 'anto.daniel@inmobi.com'},
                                       issuetype={'name': 'On-call Bug'},
#                                       components=["Grid-Infra"]
                                       )
        print issue


def main():

    instance = CreateJIRA()
    instance.enter_details()
    instance.create_jira()

if __name__ == "__main__":
    main()
=======
options = {'server':'https://jira.corp.inmobi.com', 'verify':False}
jira = JIRA(options, basic_auth=('anto.daniel','xxxxxx'))

#proj = raw_input("Enter ProjectType: ")
#print proj
#summary = raw_input("Enter Summary: ")
#print summary
#desc = raw_input("Enter Description: ")
#print desc

#summary = sys.argv[1]

issue = jira.create_issue(project={'key': ""+args.project+""}, summary=""+args.summary+"",description=""+args.description+"",issuetype={'name': 'Bug'},assignee={'name': 'anto.daniel','emailAddress': 'anto.daniel@inmobi.com'})
print issue
#user_created = issue.fields.creator
#description = issue.fields.description.title()
#print "Ticket Created by: "+user_created.__str__()+"\n"
#print "Ticket Description: "+description+"\n"
#print "Comments: "
#for comment in issue.fields.comment.comments:
#    print comment.id
#    print comment.body

>>>>>>> 2278d9b774199646a1c6739a2a421bcd417dd688
