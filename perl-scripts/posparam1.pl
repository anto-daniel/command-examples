#!/usr/bin/perl -w

print "$ARGV[0]\n";
print "$#ARGV\n";

$REQPARAM = 3;
$BADARGS = 165;
$#ARGV +=1;

unless ($#ARGV == 3) {
    print "$0 requires $REQPARAM arguments\n ";
    exit $BADARGS;
}# unless is negation of if statement

print "This script has accepted $#ARGV arguments\n";
print "@ARGV[0..$#ARGV]\n";
