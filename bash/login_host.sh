cat /tmp/hosts | while read hostname username passwd;do sshpass -p $passwd ssh $username@$hostname;done
