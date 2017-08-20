#!/bin/bash 
# redirecting all output to  a file
exec 1>testout

echo "This is a test redirecting all output"
echo "To script to another file"
echo "Without having to redirect every individual line"


