#!/usr/bin/perl -w

$DIR = "/home/antodaniel/command-examples/perl-scripts";
$FILES = "file*";
#open (HAN,"teststrings.txt") || die "die Problems: $!";
@f1 = `ls -A $FILES`;

foreach (@f1) {
    print "$_";
    chomp;
    $new = uc;
    print "$new\n";
    rename($_,$new);
}
