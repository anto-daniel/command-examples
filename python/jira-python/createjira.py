#!/usr/bin/env python
""" This Script helps in creating InMobi JIRA ticket """

from jira.client import JIRA
import argparse
import logging
import os
import urllib3

urllib3.disable_warnings()
LOGGER_NAME = 'inmobi:jira'
# Set up logging
log = logging.Logger(LOGGER_NAME, logging.INFO)
loghandler = logging.StreamHandler()
loghandler.setFormatter(logging.Formatter
                        ('%(name)s: %(levelname)s: %(message)s'))
log.addHandler(loghandler)


class CreateJIRA:
    """ Main Class """

    def __init__(self):
        """ Initial Variables """

        self.emailid = "anto.daniel@domain.com"
        options = {'server': 'https://jira.corp.domain.com', 'verify': False}
        self.jira = JIRA(options, basic_auth=('anto.daniel', 'xxxxxxxxxx'))

    def create_jira(self, args):
        """ With previous method details, creats jira ticket """

        issue = self.jira.create_issue(project={'key': ""+args.project+""},
                                       summary=""+args.summary+"",
#                                       origin=""+args.origin+"",
                                       description=""+args.description+"",
                                       assignee={'name': 'anto.daniel',
                                                 'emailAddress':
                                                 'anto.daniel@domain.com'},
                                       issuetype={'name': ""+args.type+""},
                                       components=[{'name': ""+args.component+""},],
                                       )
        log.info('JIRA Ticket ID: %s created' % issue)
#        os.system("xdg-open https://jira.corp.domain.com/browse/"+issue.__str__())


def main():

    parser = argparse.ArgumentParser("Command Line Interface for JIRA")
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='print debugging information')

    parser.add_argument("-p", "--project", help="Please specify ProjectType",
                        required=True)
    parser.add_argument("-s", "--summary", help="Please specify summary",
                        required=True)
    parser.add_argument("-d", "--description", help="Description of the issue",
                        required=True)
    parser.add_argument("-c", "--component", default='GRID Ops', help="Components of the issue",
                        required=False)
    parser.add_argument("-t", "--type", default='Nagios Alerts', help="Issue Type",
                        required=False)
 
 #   parser.add_argument("--origin", help="origin of the ticket. ex:-Ops/Production",
 #                       required=True)
    args = parser.parse_args()
    instance = CreateJIRA()
    instance.create_jira(args)

    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug('Arguments: %s', args)


if __name__ == "__main__":
    main()
