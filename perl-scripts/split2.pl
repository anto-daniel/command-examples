#!/usr/bin/perl -w


$lc = 0;


while (<>) {     ### Command Line Arguments
    print "$_";
    @array2 = split /\s+/, $_;
    #print "Elements : $array2[0..2]\n";
    foreach (@array2) {
        print  "$_\n";
    }
    $lc +=1;
}

print "Line Count = ", "\t", "$lc", "\n";
