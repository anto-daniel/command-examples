#!usr/bin/perl -w

$FILEHANDLE = "FILEREADWRITE";
#$filename = "data3";
#$appendtofile = "Append";

open ($FILEHANDLE, "ps -ef |") || die "Problems: $!";
@data1contents = <$FILEHANDLE>;
foreach(@data1contents) {
#    s/RAM/KIRAN/;
    if (/nginx.conf$/) {
        print "$_";
    }
}
#    print $FILEHANDLE $appendtofile;
