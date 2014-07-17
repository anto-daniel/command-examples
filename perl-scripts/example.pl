#!/usr/bin/perl -w 

open ("OUTFILE", ">example.txt" ) || die "Problems writing to file: $!";
$cmd_output = `cat /home/antodaniel/hosts.txt`;
print OUTFILE $cmd_output;


