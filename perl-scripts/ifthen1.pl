#!/usr/bin/perl -w

use strict;

my $var1 = "sample1";
my $var2 = "sample2";
if(1 < 2) {
    print "1 is less than 2\n";
}

if(2 == 2) {
    print "2 is equal to 2\n";
}

if($var1 eq $var2) {
    print "Both the strings are same\n";
}
else {
    print "Both are different strings\n";
}
