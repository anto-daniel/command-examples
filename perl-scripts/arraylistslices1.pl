#!/usr/bin/perl 

use strict;

my @uscities = qw(Boston Charlotte Newark Miami Austin Dulles Houston Columbia Atlanta);

print "@uscities\n";
print "@uscities[0,1]\n";
print "@uscities[0..2]\n";
print "@uscities[0..$#uscities]\n";

my @eastcoastcities = @uscities[0..3,7,8];
print ("East Coast Cities: ", "@eastcoastcities\n");
print ("Other Cities: ", "@uscities[4..6]\n");
