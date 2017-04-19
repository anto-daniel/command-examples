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

def puppet_agent_install():
   sudo("apt-get purge facter puppet puppet-common puppet-common puppetlabs-release -y")
   sudo("apt-get update")
   sudo("apt-get autoremove -y")
   sudo("apt-get install puppet puppet-common -y")
   sudo("cp /etc/hosts /etc/hosts.backup")
   sudo("echo 10.164.132.210 fab-emea01-puppet-h3 puppet puppet.actiance.local | tee -a /etc/hosts")
   sudo("sed -i '/postrun_command/ a server=fab-emea01-puppet-h3.actiance.local' /etc/puppet/puppet.conf")
   sudo('sed -i -e "$ a [agent]" /etc/puppet/puppet.conf')
   sudo('sed -i -e "$ a report=true" /etc/puppet/puppet.conf')
   sudo("puppet agent --enable")
   sudo("systemctl stop puppet")
   sudo("systemctl disable puppet")
   sudo("cd /var/lib/puppet && rm -rfv ssl/")
   sudo("mkdir -v -p /apps && chown -v -R appsuser:appsuser /apps")

def prepare_deploy():
    #local("./manage.py test my_app")
    #local("git pull")
    local("git add --all") 
    local("git config --global user.name 'Anto Daniel'")
    local("git config --global user.email 'anto.daniel@gmail.com'")
    result = local("git commit -m 'fab deployed'")
    if result.return_code == 0:
        local("git push origin master")
        print "Pushed to Git Successfully !!! :)"
    elif result.return_code == 1:
        print "No commit found"
    else:
        print "Errors found during commit"

def install_disk_prepare(user=env.user):
    sudo('apt-get install python-dev python-pip libffi-dev -y')
    sudo('pip install paramiko cryptography==1.2.1')
    run('mkdir -p $HOME/DiskPrepare/')
    put('DiskPrepare.py','/home/'+env.user+'/DiskPrepare')
    put('PartitionandMount.py','/home/'+env.user+'/DiskPrepare')
    run('cd DiskPrepare && python DiskPrepare.py')
    run('cd DiskPrepare && python PartitionandMount.py')

def puppet_agent_1604():
    #sudo("apt-get purge --auto-remove puppet-common")
    #sudo("apt-get purge --auto-remove puppetlabs-release")
    #sudo("apt-get install -y puppet-common=3.8.5-2")
    #sudo("sudo apt-get -y install puppet=3.8.5-2")
    sudo("puppet agent --enable")
    sudo("systemctl stop puppet")
    sudo("systemctl disable puppet")
    #sudo("systemctl status puppet")
    #sudo("sed -i 's/server=.*/server=fab-prod02-puppet-h5\.actiance\.local/' /etc/puppet/puppet.conf")
    sudo("apt-get install mcollective -y")
    sudo("puppet agent --environment=agent --debug --test")
    sudo("systemctl restart mcollective")

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
    env = run("hostname | awk -F- '{print $2}'")
    sudo('apt-get install nfs-common -y')
    sudo('mkdir -p /nfs-path/{failedxml,stormexports}')
    sudo('echo "fab-'+env+'-nfs-h2:/data1/failedxml   /nfs-path/failedxml   nfs rw,exec,user   0     0" | tee -a /etc/fstab')
    sudo('echo "fab-'+env+'-nfs-h2:/data1/stormexports   /nfs-path/stormexports   nfs rw,exec,user   0     0" | tee -a /etc/fstab')
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
    put('townsend_keys','/tmp')
    sudo('rm -rfv /apps/config/keystore/*')
    sudo('cp -rfv /tmp/townsend_keys/* /apps/config/keystore')

def usermod_appsuser():
    sudo('usermod -s /bin/bash appsuser')
    sudo("echo -e \"alcatraz1400\nalcatraz1400\n\" | passwd appsuser")
    sudo("usermod -a -G sudo appsuser")

def glib_vulnerable():
    put('a.out','/home/sysops')
    sudo('chmod a+x a.out')
    sudo('./a.out')

def add_puppet_host():
    sudo('sed -i "$ a 192.168.126.153 puppet.actiance.local" /etc/hosts')

def passwdless_authentication():
   sudo('su -c "./passwdless_auth.sh" -s /bin/bash appsuser')

def backup():
    sudo('cp -rfv /apps /opt')
def install_tokenizer():
    sudo('/usr/share/elasticsearch/bin/plugin install file:///tmp/actiance-standard-tokenizer-1.0.zip --verbose')
    sudo('/usr/share/elasticsearch/bin/plugin list')

def start_elastic():
    sudo('service elasticsearch start')
    sudo('service elasticsearch status')

def stop_hazelcast():
    sudo('systemctl stop hazelcast')

def start_hazelcast():
    sudo('systemctl start hazelcast')

def stop_storm():
    sudo('systemctl stop stormsupervisor')
    sudo('systemctl stop stormnimbus')
    sudo('systemctl stop stormui')

def start_storm():
    sudo('systemctl start stormsupervisor')
    sudo('systemctl start stormnimbus')
    sudo('systemctl start stormui')

def stop_karaf():
    sudo('systemctl stop karaf')

def start_karaf():
    sudo('systemctl start karaf')

def stop_supervisor():
    sudo('systemctl stop stormsupervisor')

def start_supervisor():
    sudo('systemctl start stormsupervisor')

def add_keyfile_to_mongo():
    sudo('echo --auth = true | tee -a /lib/systemd/system/mongodb.service')
    sudo('echo --keyFile =  /etc/ssl/mongokeyfile | tee -a /lib/systemd/system/mongodb.service')
    run('cat /lib/systemd/system/mongodb.service')

def del_line_to_mongo():
    sudo("sed -i '$ d' /lib/systemd/system/mongodb.service")

def mongo_auth_router():
    sudo("sed -i '/ExecStart/ s/$/\ --keyFile  \/etc\/ssl\/mongokeyfile/' /lib/systemd/system/mongodb.service")
    sudo("systemctl daemon-reload")
    #sudo("sed -i '/ExecStart/ s/--auth = true --keyFile =  \/etc\/ssl\/mongokeyfile/--auth true --keyFile \/etc\/ssl\/mongokeyfile/' /lib/systemd/system/mongodb.service")
    #sudo("sed -i '/ExecStart/ s/--auth true//' /lib/systemd/system/mongodb.service")
    put('/tmp/mongokeyfile','/tmp')
    sudo('cp -rfv /tmp/mongokeyfile /etc/ssl')
    sudo('chmod 400 /etc/ssl/mongokeyfile')
    sudo('chown appsuser:appsuser /etc/ssl/mongokeyfile')
    sudo('systemctl start mongodb')
    #run('cat /lib/systemd/system/mongodb.service')

def change_auth():
    sudo('sed -i "/server.mongo.auth.enabled/ s/false/true/" /apps/karaf_nfs/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -i "/JQ24Zfw31VTGH3Pecg8.zQ==/ s/password=.*/pr8d8CSVJI1yRPlSk1GHxA==/g" /apps/karaf_nfs/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -i "/server.mongo.auth.enabled/ s/false/true/" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -i "/JQ24Zfw31VTGH3Pecg8.zQ==/ s/password=.*/password=pr8d8CSVJI1yRPlSk1GHxA==/g" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -i "/server.mongo.auth.enabled/ s/false/true/" /apps/alcatraz_cache-1.0/conf/server.properties')
    sudo('sed -i "/JQ24Zfw31VTGH3Pecg8.zQ==/ s/password=.*/password=pr8d8CSVJI1yRPlSk1GHxA==/g" /apps/alcatraz_cache-1.0/conf/server.properties')
    sudo('sed -i "/server.mongo.auth.enabled/ s/false/true/" /apps/storm-1.0.2/conf/server.properties')
    sudo('sed -i "/JQ24Zfw31VTGH3Pecg8.zQ==/ s/password=.*/password=pr8d8CSVJI1yRPlSk1GHxA==/g" /apps/storm-1.0.2/conf/server.properties')
    
def push_dr_hosts():
    put('drhosts','/tmp')
    sudo('cat /tmp/drhosts | tee -a /etc/hosts')

def push_p_hosts():
    put('phosts','/tmp')
    sudo('cat /tmp/phosts | tee -a /etc/hosts')

def push_mongo_keyfile_computes():
    put('mongokeyfile','/tmp')
    sudo('cp -rfv /tmp/mongokeyfile /etc/ssl')
    sudo('chmod 400 /etc/ssl/mongokeyfile')
    sudo('chown -v appsuser:appsuser /etc/ssl/mongokeyfile')

def push_mongo_service_script():
    put('mongod.service','/tmp')
    put('mongodb.service','/tmp')
    sudo('cp -rfv /tmp/mongod.service /lib/systemd/system/')
    sudo('cp -rfv /tmp/mongodb.service /lib/systemd/system/')
    sudo('systemctl daemon-reload')
    sudo('systemctl stop mongodb')
    sudo('systemctl stop mongod')
    sudo('rm -rfv /tmp/mongo*.sock')
    sudo('systemctl start mongodb')
    sudo('systemctl start mongod')

def push_ceph_keys_to_computes():
    put('ceph.tar.gz','/tmp')
    sudo('rm -rfv /etc/ceph/*')
    sudo('tar xvzf /tmp/ceph.tar.gz -C /etc/ceph')
    sudo('chown -v -R appsuser:appsuser /etc/ceph')

def push_keystore():
    put('.keystore','/tmp')
    sudo('mv /tmp/.keystore /apps/karaf/etc/security')
    sudo('chown appsuser:appsuser /apps/karaf/etc/security/.keystore')
    sudo('ls -la /apps/karaf/etc/security/.keystore')

def change_sp_karaf():
    sudo('sed -n "/fab-emea01-twn/ p" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -i "s/fab-emea01-twn-h1/fab-emea01-twn-h2/g" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')
    sudo('sed -n "/fab-emea01-twn/ p" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')

def change_sp():
    fab = run("hostname | awk -F- '{print $3}'")
    #print fab
    if fab == "haz":
        print "hazelcast"
    if fab == "stm":
        print "storm"
    if fab == "karafui" or fab == "karafdig":
        print "karaf"
        put('server.properties','/tmp')
        sudo("cp -rfv /tmp/server.properties /apps/karaf/etc/actiance/apc-system/apc-config/")
        #sudo("sed -i '$ a 10.164.111.186  vip-jpemea01-egw01' /etc/hosts")
    if fab == "nfs":
        print "nfs"


    
def add_host_entry(ip,hostname):
    sudo('sed -i "$ a '+ip+' '+hostname+' devtest06.dig.jpmc.actiance.net" /etc/hosts')

def change_service_script():
    fab = run("hostname | awk -F- '{print $3}'")
    #print fab
    if fab == "haz":
        sudo('sed -i "s/64000/65535/" /lib/systemd/system/hazelcast.service')
        sudo("systemctl daemon-reload")
    if fab == "stm":
        sudo('sed -i "s/64000/65535/" /etc/systemd/system/stormnimbus.service')
        sudo('sed -i "s/64000/65535/" /etc/systemd/system/stormsupervisor.service')
        sudo('sed -i "s/64000/65535/" /etc/systemd/system/stormnimbus.service')
        sudo("systemctl daemon-reload")
    if fab == "karafui" or fab == "karafdig":
        sudo('sed -i "s/64000/65535/" /etc/systemd/system/karaf.service')
        sudo("systemctl daemon-reload")
    if fab == "nfs":
        sudo('sed -i "s/64000/65535/" /lib/systemd/system/karaf.service')
        sudo("systemctl daemon-reload")

def change_server_property_value(key,value):
    fab = run("hostname | awk -F- '{print $3}'")
    if fab == "haz":
        sudo('sed -i "/'+key+'/ s/'+key+'=.*/'+key+'='+value+'/g" /apps/alcatraz_cache-1.0/conf/server.properties')
    if fab == "stm":
        sudo('sed -i "/'+key+'/ s/'+key+'=.*/'+key+'='+value+'/g" /apps/storm-1.0.2/conf/*.properties')
    if fab == "karafui" or fab == "karafdig":
        sudo('sed -i "/'+key+'/ s/'+key+'=.*/'+key+'='+value+'/g" /apps/karaf/etc/actiance/apc-system/apc-config/server.properties')
    if fab == "nfs":
        sudo('sed -i "/'+key+'/ s/'+key+'=.*/'+key+'='+value+'/g" /apps/karaf_nfs/etc/actiance/apc-system/apc-config/server.properties')




