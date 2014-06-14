#!/usr/bin/perl -w

$min = 1;
$max = 20;
$fullname = "Dean Davis";

open (OUTFILE, ">data1") || die "Problems: $!";
for ($min..$max) { print OUTFILE "$fullname\n"; }
