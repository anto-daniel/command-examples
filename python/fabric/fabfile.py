#!/usr/bin/env python

from fabric.api import local
from fabric.api import run, sudo
from fabric.api import env, put

#env.hosts = ['192.168.112.16', '192.168.120.44']
env.user = "sysops"
env.password = "alcatraz1400"
env.warn_only = True
env.skip_bad_hosts = True

def hello(who="world"):
    print "Hello {who}!".format(who=who)

def prepare_deploy():
    #local("./manage.py test my_app")
    #local("git pull")
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
    sudo('tar xvzf /tmp/storm-bin-scripts.tar.gz -C /')
    run('rm -rfv /tmp/storm-bin-scripts.tar.gz')

def rescan_scsi():
    sudo('apt-get install scsitools -y')
    sudo('rescan-scsi-bus')

def push_ceph():
    sudo('rm -rfv /tmp/ceph')
    put('ceph/ceph','/tmp')
    sudo('rm -rfv /etc/ceph/*')
    sudo('cp -rfv /tmp/ceph/* /etc/ceph')

def push_townsend():
    put('/home/sysops/townsend/admin_one_keystore.jks','/tmp')
    sudo('cp -rfv /tmp/admin_one_keystore.jks /apps/config/keystore/')
    put('/home/sysops/townsend/CATrustStore.jks','/tmp')
    sudo('cp -rfv /tmp/CATrustStore.jks /apps/config/keystore/')
    put('/home/sysops/townsend/client_actiance_cert_keystore.jks','/tmp')
    sudo('cp -rfv /tmp/client_actiance_cert_keystore.jks /apps/config/keystore/')

def push_karaf_script():
    put('karaf','/tmp')
    sudo('cp -rfv /tmp/karaf /etc/init.d/')
    sudo('rm -rfv /tmp/karaf')
    result = run('hostname')
    print 'Pushing karaf script in host '+result
    if "araf" in result:
        print "karaf host"
    elif "nfs" in result:
        sudo("sed -i 's/karaf_apc/karaf_nfs/g' /etc/init.d/karaf")
    else:
        print "Not a valid host"

def install_nfs():
    print "Install NFS Package in NFS Server ........"
    sudo('apt-get install nfs-kernel-server nfs-common -y')
    print "Appending data entry in exports file"
    sudo('if [[ ! $(grep data1 /etc/exports) ]];then echo "/data1 *(rw,no_root_squash,no_all_squash,sync,no_subtree_check)" | tee -a /etc/exports;fi')
    sudo('service nfs-kernel-server restart')
    sudo('exportfs')
    sudo('mkdir -p /data1/{failedxml,stormexports}')

def push_ingestion_doc_scripts():
    put('ingest_document.tar.gz','/tmp')
    run('tar xvzf /tmp/ingest_document.tar.gz -C $HOME')

def ganglia_modules():
    print "Pushing the puppet modules to the Server...."
    put('ganglia_puppet_installation.tar.gz','/tmp')
    print "Extracting Ganglia modules in Puppet Environment...."
    sudo('tar xvzf /tmp/ganglia_puppet_installation.tar.gz -C /')
 
def push_data_mount_point():
    sudo('apt-get install nfs-common -y')
    sudo('mkdir -p /nfs-path/{failedxml,stormexports}')
    sudo('echo "fab-storlab-nfs-h1:/data1/failedxml   /nfs-path/failedxml   nfs rw,exec,user   0     0" | tee -a /etc/fstab')
    sudo('echo "fab-storlab-nfs-h1:/data1/stormexports   /nfs-path/stormexports   nfs rw,exec,user   0     0" | tee -a /etc/fstab')
    sudo('mount -a')
    run('df -h')

def set_ulimit():
    sudo('echo "*               soft    nofile          65535" | tee -a /etc/security/limits.conf')
    sudo('echo "*               hard    nofile          65535" | tee -a /etc/security/limits.conf')
    sudo('echo "*               soft    nproc           65535" | tee -a /etc/security/limits.conf')
    sudo('echo "*               hard    nproc           65535" | tee -a /etc/security/limits.conf')
    sudo('sysctl -p')

def check_disk():
    run('df -h /data* /logs')


def lsblk():
    sudo('lsblk')

def create_app_user():
    sudo('adduser appsuser  --home /apps --disabled-password --disabled-login --gecos "" --shell /bin/false')

def create_ceph_user():
    sudo('echo -e "ceph\nceph\n" | adduser appsuser  --home /apps --gecos "" --shell /bin/sh')

def run_puppet_agent():
    sudo('puppet agent -t --environment=QA --debug')

def install_puppet_ganglia_agent():
    sudo('puppet agent -t --environment=development --debug')
    sudo('service ganglia-monitor restart')


def copy_townsend_keys():
    sudo('cp -rfv /tmp/keystore /apps/config')

def usermod_appsuser():
    sudo('usermod -s /bin/bash appsuser')
    sudo("echo -e \"alcatraz1400\nalcatraz1400\n\" | passwd appsuser")
    sudo("usermod -a -G sudo appsuser")

def glib_vulnerable():
    put('a.out','/home/sysops')
    sudo('chmod a+x a.out')
    sudo('./a.out')
