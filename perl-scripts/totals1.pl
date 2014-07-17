#!/usr/bin/perl 
use warnings;
use strict;

my $data1 = "dataproducts1";
open (han1, "$data1") || die "Errors opening file $data1: $!";
my @f1 = <han1>;
my $total = 0;

foreach(@f1) {
#    print "$_";
    my @columns = split;
#    print $columns[4], "\n";
    $total = $columns[3] + $total;
    
}
print "Grand Total of all products: ", $total, "\n";
