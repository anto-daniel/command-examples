#!/usr/bin/perl -w

$DIR = "/etc";
$DIRHANDLE = "HANDLE";
@dirlist = `ls -A $DIR`;

#opendir ($DIRHANDLE, "$DIR") || die "Error opening $DIR: $!";
#@dirlist = readdir($DIRHANDLE);

foreach (@dirlist) {
    print "$_";
}
