#!/usr/bin/perl -w

#$min = 1;
#$max = 20;
#$fullname = "Anto Daniel";
@array1 = qw(Anto Rahul Manzoor Ragh Chida Rajini);
#open (INFILE, "data2") || die "Problems: $!";
open (OUTFILE, ">>data1") || die "Problems: $!";

foreach (@array1) { print OUTFILE "$_\n"; } 
