#!/usr/bin/env python
""" This Script helps in creating InMobi JIRA ticket """

import sys
import getopt
from jira.client import JIRA


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
