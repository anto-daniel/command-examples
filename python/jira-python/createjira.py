#!/usr/bin/env python
""" This Script helps in creating InMobi JIRA ticket """

import sys
import getopt
from jira.client import JIRA
import argparse

class CreateJIRA:
    """ Main Class """

    def __init__(self):
        """ Initial Variables """

        self.emailid = "anto.daniel@inmobi.com"
        options = {'server': 'https://jira.corp.inmobi.com', 'verify': False}
        self.jira = JIRA(options, basic_auth=('anto.daniel', 'Rachel@123'))


    def create_jira(self, args):
        """ With previous method details, creats jira ticket """

        issue = self.jira.create_issue(project={'key': ""+args.project+""},
                                       summary=""+args.summary+"",
                                       description=""+args.description+"",
                                       assignee={'name': 'anto.daniel',
                                                 'emailAddress': 'anto.daniel@inmobi.com'},
                                       issuetype={'name': 'On-call Bug'},
#                                       components=["Grid-Infra"]
                                       )
        print issue


def main():

    parser = argparse.ArgumentParser("Please specify the details")
    parser.add_argument("--project", help="Please specify ProjectType", required=True)
    parser.add_argument("--summary", help="Please specify summary", required=True)
    parser.add_argument("--description", help="Description of the issue", required=True)
    args = parser.parse_args()
    instance = CreateJIRA()
    instance.create_jira(args)

if __name__ == "__main__":
    main()
