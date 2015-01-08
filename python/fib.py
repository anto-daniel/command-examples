#!/usr/bin/env python
import argparse
import logging

LOGGER_NAME = "fibnoacci"
log = logging.Logger(LOGGER_NAME, logging.INFO)
loghandler = logging.StreamHandler()
loghandler.setFormatter(logging.Formatter('%(name)s: %(levelname)s: %(message)s'))
log.addHandler(loghandler)


parser = argparse.ArgumentParser()
parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='print debugging information')
parser.add_argument("--number", type=int, help="Please enter number")
args = parser.parse_args()

n = args.number

def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

if args.debug:
    log.setLevel(logging.DEBUG)

log.debug('Arguments: %s', args)

log.info("Answer: %s" % fib(n))

