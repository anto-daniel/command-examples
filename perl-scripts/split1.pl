#!/usr/bin/perl -w

$data4 = "Anto:Daniel"; #Scalar value
@array1 = split /:/, $data4;

$lc = 0;

foreach(@array1) {
    print "$_\n";
}

#print "$array1[0]","\n";
while (<>) {     ### Command Line Arguments
    print "$_";
    @array2 = split /:/, $_;
    $lc +=1;
}

print "Line Count = ", "\t", "$lc", "\n";
