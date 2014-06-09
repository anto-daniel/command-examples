#!/usr/bin/perl 

@array1 = (["1","2"],["3","4"],["5","6"]);
$array1ref = [["1","2"],["3","4"],["5","6"]]; #multidimensional array 
    
print "output1: $array1ref->[0][0]\n";
print "output2: $array1[1][1]\n";

open(HAN1,"data1") || die "Errors opening data1: $!";

while (<HAN1>) {
    push @array2, [ split ];
}

foreach (@array2) {
    print "@$_\n";
}
