#!/usr/bin/env python

from fabric.api import local
from fabric.api import run, sudo
from fabric.api import env, put

#env.hosts = ['192.168.112.16', '192.168.120.44']
env.user = "apcuser"
env.password = "facetime"
env.warn_only = True

def hello(who="world"):
    print "Hello {who}!".format(who=who)

def prepare_deploy():
    #local("./manage.py test my_app")
    local("git add --all") 
    local("git config --global user.name 'Anto Daniel'")
    local("git config --global user.email 'anto.daniel@gmail.com'")
    result = local("git commit -m 'fab deployed'")
    if result.return_code == 0:
        local("git push")
        print "Pushed to Git Successfully !!! :)"
    elif result.return_code == 1:
        print "No commit found"
    else:
        print "Errors found during commit"

def test():
    run('ls')


def install_disk_prepare(user=env.user):
    sudo('apt-get install python-dev python-pip libffi-dev -y')
    sudo('pip install paramiko cryptography==1.2.1')
    run('mkdir -p $HOME/DiskPrepare/')
    put('DiskPrepare.py','/home/'+env.user+'/DiskPrepare')
    put('PartitionandMount.py','/home/'+env.user+'/DiskPrepare')
    run('cd DiskPrepare && python DiskPrepare.py')
    run('cd DiskPrepare && python PartitionandMount.py')

def extract_storm_start_up_scripts(user=env.user):
    put('storm_start_scripts.tar.gz','/tmp')
    sudo('tar xvzf /tmp/storm_start_scripts.tar.gz -C /')
    sudo('rm -rfv /tmp/storm_start_scripts.tar.gz')

def extract_storm_bin_dir(user=env.user):
    print "Uploading Storm Bin directory to resp hosts..."
    put('storm-bin-scripts.tar.gz','/tmp')
    print "Extracting Storm bin directory"
    run('tar xvzf /tmp/storm-bin-scripts.tar.gz -C $HOME')
    run('rm -rfv /tmp/storm-bin-scripts.tar.gz')

def rescan_scsi():
    sudo('apt-get install scsitools')
    sudo('rescan-scsi-bus')

def push_karaf_script():
    put('karaf','/tmp')
    sudo('cp -rfv /tmp/karaf /etc/init.d/')
    sudo('rm -rfv /tmp/karaf')

