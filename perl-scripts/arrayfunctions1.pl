#!/usr/bin/perl -w

use strict;

my $firstname = "Dean";
my $middlename = "Andrew";
my $lastname = "Davis";

my @array1 = ("New York","New Jersey","Conneticut");
print "@array1\n";

my $ppop = pop @array1;
print "@array1\n";

push @array1, $ppop;
print "The array now contains:", "@array1\n";

push @array1, $firstname;
print "The array now contains:", "@array1\n";

unshift (@array1,"$firstname","$middlename","$lastname"); #add the contents of $firstname to array1
print "After using unshift: ", "@array1\n";

shift @array1; # remove the value from the first element from the array
print "After using shift: ","@array1\n";

my @array1 = sort @array1;
print "After using sort: ", "@array1\n";
