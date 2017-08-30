#!/bin/bash


nfs_failedxml_dir='/data1/failedxml'
#tenant=$1
failedxml_dir="\/data1\/stormexports\/input\/"
cwd=$(pwd)

#if [[ $tenant == "" ]]
#then
#  echo -e "Usage: $0 <tenant-name>"
#  exit 1
#fi

oldest_date=$(cd $nfs_failedxml_dir && for dir in $(ls -1);do ls -1 $dir;done | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}" | sort | uniq | head -1)
echo $oldest_date
#oldest_date=$(ls -1 $nfs_failedxml_dir/$tenant | sort -n | head -1)
old_1day_ago=$(date -d "$oldest_date 1 day ago" +'%F')
epoch_date=$(date -d "$old_1day_ago" +%s)
today=$(date +%Y-%m-%d)
yday=$(date -d '1 day ago' +%Y-%m-%d)
yyday=$(date -d '2 day ago' +%Y-%m-%d)
nday=$(date -d 'next day' +%Y-%m-%d)
####   Wait to drain all the ingestion pipelines ###

echo -e "INFO: Wait ingestion pipeline to drain messages..."
./drain_lag.sh ingestionconsumers rs1 fab-jpuat01-kafzoo-h2:2471
if [ $? -eq 0 ]; then echo -e "\nINFO: rs1 pipeline messages drained\n"; else echo "error";exit 1;fi
echo -e "INFO: Wait lfs pipeline to drain messages..."
./drain_lag.sh ingestionlfsconsumers lfs fab-jpuat01-kafzoo-h2:2471
if [ $? -eq 0 ]; then echo -e "\nINFO: lfs pipeline messages drained\n"; else echo "error";exit 1;fi




rm -rfv *.csv *.txt

###### To find out the tenants from mongodb ####

echo -e "INFO: Getting the tenants information"
mongoexport --port 23757 --ssl --sslAllowInvalidCertificates  -u 'admin' -p 'alcatraz1400' --authenticationDatabase 'admin' --db alcatraz --collection tenancy --fields "_id,tenantName" --type csv --out tenantinfo.csv
sed -i 's/,/\ /g' tenantinfo.csv
sed -i '1 d' tenantinfo.csv
cat tenantinfo.csv

#### Getting FailedXML Information from mongo
cat tenantinfo.csv | while read -r id tenantName
do
        mongoexport --port 23757 --ssl --sslAllowInvalidCertificates -u 'admin' -p 'alcatraz1400' --authenticationDatabase 'admin' --db $id --collection failed_messages --fields eventinfo --type=csv --query "{'processedtime' : {\$gt:${epoch_date}000}}" >> ${cwd}/failed_messages.csv
done
awk -f $cwd/find_donot_delete.awk $cwd/failed_messages.csv >> $cwd/donot_delete_temp.txt
cat donot_delete_temp.txt | sort | uniq >> $cwd/do_not_delete_file_list.txt
sed -i "s/^/$failedxml_dir/g;s/\ /\//g" $cwd/do_not_delete_file_list.txt

#### Getting Complete file list from Directory: "/data1/stormexports/input"
find "/data1/stormexports/input" -name "*" -type f >> $cwd/complete_file_list_temp.txt
cat $cwd/complete_file_list_temp.txt | sort | uniq >> $cwd/complete_file_list.txt
comm -23 $cwd/complete_file_list.txt $cwd/do_not_delete_file_list.txt >> $cwd/should_delete_file_list_temp.txt

####  Final list of files to be deleted excluding past 3 days

egrep -v "${today}|${yday}|${yyday}|${nday}" $cwd/should_delete_file_list_temp.txt >> $cwd/should_delete_file_list.txt

## Cleaning up the files from should_delete_file_list.txt
/bin/bash $cwd/cleanup.sh

### Cleaning up the unneeded files ####
/bin/rm -rfv $cwd/*.csv $cwd/*.txt
