import sys, getopt
from jira.client import JIRA
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ticketid", help="Enter TicketID. example: OPS-5432")
parser.add_argument("--comment",help="Please comment")
args = parser.parse_args()



options = {'server':'https://jira.corp.inmobi.com','verify':False}

jira = JIRA(options, basic_auth=('anto.daniel','Paul@123'))

ticketid = args.ticketid
addcomment = args.comment

comment = jira.add_comment(ticketid, addcomment)
print 'added comment'
