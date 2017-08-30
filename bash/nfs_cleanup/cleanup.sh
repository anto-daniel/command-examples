#!/bin/bash
rm -f success.file
rm -f failure.file
cat should_delete_file_list.txt | while read file; do
echo "Working on $file";
rm "$file";
rc=$?
if [[ $rc -eq 0 ]]; then
   echo $file >> success.file
else
  echo $file >> failure.file
fi
done
