#!/usr/bin/perl -w

$FILEHANDLE = "FILEREADWRITE";
$filename = "data3";
$appendtofile = "Append";

open ($FILEHANDLE, "+<$filename") || die "Problems: $!";
@data1contents = <$FILEHANDLE>;
foreach(@data1contents) {
    s/RAM/KIRAN/;
    print "$_";
}
#    print $FILEHANDLE $appendtofile;
