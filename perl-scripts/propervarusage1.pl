#!/usr/bin/perl

use strict;

#my $firstname = "Dean";  # Lexical Variable
my $age = 29;            # Lexical Variable
our $count = 1;          # Global Variable
our $_101park = 101;
    print "Please tell us your first name","\n";
    my $firstname = <STDIN>;
    print "$firstname is $age years young","\n";
    print "Count is set to: ", "$count", "\n";
    print "$_101park", "\n";

# Block Definition
{
    my $firstname = "Dumil";
    my $age = 2;
    print "$firstname is $age years young", "\n";
}

    print "firstname is now: ","$firstname\n"
