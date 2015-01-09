#!/usr/bin/env python
""" This Script helps in creating InMobi JIRA ticket """

from jira.client import JIRA
import argparse
import logging

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

        self.emailid = "anto.daniel@inmobi.com"
        options = {'server': 'https://jira.corp.inmobi.com', 'verify': False}
        self.jira = JIRA(options, basic_auth=('anto.daniel', 'xxxxxxxx'))

    def create_jira(self, args):
        """ With previous method details, creats jira ticket """

        issue = self.jira.create_issue(project={'key': ""+args.project+""},
                                       summary=""+args.summary+"",
                                       description=""+args.description+"",
                                       assignee={'name': 'anto.daniel',
                                                 'emailAddress':
                                                 'anto.daniel@inmobi.com'},
                                       issuetype={'name': 'On-call Bug'},
                                       )
        log.info('JIRA Ticket ID: %s created' % issue)


def main():

    parser = argparse.ArgumentParser("Command Line Interface for JIRA")
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='print debugging information')

    parser.add_argument("--project", help="Please specify ProjectType",
                        required=True)
    parser.add_argument("--summary", help="Please specify summary",
                        required=True)
    parser.add_argument("--description", help="Description of the issue",
                        required=True)
    args = parser.parse_args()
    instance = CreateJIRA()
    instance.create_jira(args)

    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug('Arguments: %s', args)


if __name__ == "__main__":
    main()
