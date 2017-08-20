#!/usr/bin/perl 

use warnings;
use strict;

open (han1, ">> logfile.sub") || die "Errors opening file: $!";
my $etcdir = `ls -l /etc/passwd`;
chomp $etcdir;
my $message = "Launching sub2.pl";

log_message("$message");
log_message("$etcdir");

sub log_message {
    my $current_time = localtime;
    print "$current_time - $_[0]", "\n";
    print han1 "$current_time - $_[0]", "\n";
}
