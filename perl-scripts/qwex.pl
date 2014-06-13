#!/usr/bin/perl -w

use strict;

my @array = qw(This is a list of words without interpolation);

foreach my $key (@array) {
    print "Key is $key\n";
}
