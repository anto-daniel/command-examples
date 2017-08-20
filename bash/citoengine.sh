#! /bin/bash

NAGIOS_DIR=/usr/local/nagios/
NAGIOS_CONF=$NAGIOS_DIR/etc
CITO_FILE=gridd.csv
NCONF_DIR=/var/www/html/nconf
NCONF_DPL=$NCONF_DIR/ADD-ONS
SERVICES=`awk -F, '/^[0-9]+/ {print $7}' gridd.csv`

cp $NAGIOS_CONF/Default_collector/services.cfg $HOME/cito_backup/services.cfg.bak-`date +%d-%m-%Y-%H-%M`
cp $NAGIOS_CONF/Default_collector/hosts.cfg $HOME/cito_backup/hosts.cfg.bak-`date +%d-%m-%Y-%H-%M`
cp $NAGIOS_CONF/global/contactgroups.cfg $HOME/cito_backup/contactgroups.cfg.bak-`date +%d-%m-%Y-%H-%M`

if [ ! -f ${CITO_FILE} ] ; then
echo "please generate new $CITO_FILE File from CitoEngine and upload to the dpath /var/www/nconf/ADD-ONS"
exit 0;
fi
cd $NCONF_DPL
/usr/bin/python ./cito_config_parser.py --type nagios -c $NAGIOS_CONF/Default_collector/services.cfg --events-file $CITO_FILE --generate --out $NAGIOS_CONF/Default_collector/new_services.cfg >>error.log
value=`echo $?`
if [ "$value" -eq 0 ] ; then

  echo "creating new services.cfg and hosts.cfg  files with CITOENGINE parameters"

  ## adding service event codes to services.cfg file
  mv $NAGIOS_CONF/Default_collector/new_services.cfg $NAGIOS_CONF/Default_collector/services.cfg
  chown www-data:www-data $NAGIOS_CONF/Default_collector/services.cfg

  ## adding host event code to hosts.cfg file
  sudo sed -ie '/host_name/a\'$'\n \_CITOEVENTID 7\n' $NAGIOS_CONF/Default_collector/hosts.cfg
  #sudo sed -i '/host_name/a _CITOEVENTID      7' $NAGIOS_CONF/Default_collector/hosts.cfg
  chown nagios:nagios $NAGIOS_CONF/Default_collector/hosts.cfg
  awk -F, '/^[0-9]+/ {print $7}' gridd.csv > services.txt
  services=$(echo `cat services.txt | sed 's/\r/\ /g'`)
  for srv in $services;do
    #echo $srv  
    lns=`cat services.cfg | egrep -n -A8 "$srv" | egrep "contact_groups" | grep -v noc-mon | awk -F- '{print $1}'`
	  for ln in $lns; do 
	    echo $ln
	    sed -ie "${ln}s/$/,noc-mon-alerts/g" $NAGIOS_CONF/Default_collector/services.cfg
	    sed -n "${ln} p" $NAGIOS_CONF/Default_collector/services.cfg
	  done
  done
	sed -ie "/}/a\ \ndefine noc-mon {\n\t\tcontact_name\tnoc-mon\n\t\talias\t\tnoc-mon\n\t\thost_notification_options\td\n\t\tservice_notification_options\tc\n\t\temail\t\tnoc-mon@inmobi.com\n\t\thost_notification_period\t24x7\n\t\thost_notification_commands\t24x7\n\t\thost_notification_commands notify-host-by-email\n\t\tservice_notification_commands\tnotify-service-by-email \n}" $NAGIOS_CONF/global/contacts.cfg
  ## adding citoengine contact group to the contactgroups.cfg file
  #sed -i 's/adserve.engg.oncall/adserve.engg.oncall,citoengine/g' $NAGIOS_CONF/global/contactgroups.cfg
  /etc/init.d/nagios reload
else
  rm $NAGIOS_CONF/Default_collector/new_services.cfg
  echo "please generate new $CITO_FILE File from Cito Engine and upload to the path /var/www/nconf/ADD-ONS/"
fi
