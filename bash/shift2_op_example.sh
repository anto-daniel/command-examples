#!/bin/bash
if [ $# -lt 1 ]; then
        echo "Usage: $0 package(s)"
        exit 1
fi
while (($#)); do
	yum install "$1" << CONFIRM
y
CONFIRM
shift
done
