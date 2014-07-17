#!/usr/bin/perl -w

#$min = 1;
#$max = 20;
#$fullname = "Dean Davis";
#@array1 = qw(Anto Rahul Manzoor Ragh Chida Rajini);
$IN = "INFILE";
$OUT = "OUTFILE";
$filenamein = "data1";
$filenameout = "data2";
open ($IN, "$filenamein") || die "Problems: $!";
open ($OUT, ">$filenameout") or die "Problems writing to file: $!";
@data1contents = <$IN>;
#foreach (@array1) { print OUTFILE "$_\n"; } 

#while(<$IN>) {
#    print "$_";
#}

foreach (@data1contents) {
    s/Rajini/Rajinikanth/;
    if (/Rajini/) {
        print $OUT "$_";
    }
}
