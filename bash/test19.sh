#!/bin/bash 

tempfile=`mktemp test19.XXXXXX`
exec 3>$tempfile
echo "This script writes to a temp file: $tempfile"
echo "This is the first line" >&3
echo "This is the second line" >&3
echo "This is the last line" >&3
exec 3>&-

echo "Done creating the tempfile. The contents are:"
cat $tempfile
rm -f $tempfile 2> /dev/null

