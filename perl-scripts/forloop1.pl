#!/usr/bin/perl -w

#$min = 1;
#$max = 10;
#$PROD_NAME = "Linux CBT Scripting Edition";
@array1 = ("Dean","LinuxCBT","Scripting","Debian","RedHat");
#for ($i=$min; $i<=$max; $i++) {
#    print "$i\n";
#}

#for ($min..$max) {print "$PROD_NAME\n"; }
foreach (@array1) {
    print "$_\n";
}# foreach is usually used for array
    $#array1 +=1;
    print "Total Elements of Array = $#array1\n";
