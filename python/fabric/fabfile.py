#!/usr/bin/env python

from fabric.api import local
from fabric.api import run
from fabric.api import env

env.hosts = ['192.168.112.16', '192.168.120.44']
env.user = "apcuser"
env.password = "facetime"

def hello(who="world"):
    print "Hello {who}!".format(who=who)

def prepare_deploy():
    #local("./manage.py test my_app")
    local("git add --all && git commit -m 'fab deployed'")
    local("git push")

def test():
    run('ls')

