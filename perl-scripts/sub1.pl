#!/usr/bin/perl 

use strict;
testsub("Dean","Davis");

sub testsub {
    #  my $name = "Dean Davis";
    #  print "Hello ","$name\n";
    #  print "Hello ", "$_[0]\n";
    foreach(@_) {
        print "Hello ", "$_\n";
    }
        print "Hello ", "@_\n";
}

