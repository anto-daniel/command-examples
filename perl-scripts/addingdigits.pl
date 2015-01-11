#!/usr/bin/perl 

print "Hello Program !!!!\n";

my $number = "$ARGV[0]\n";
sub recur {
    my $num = shift;
    chomp($num);
    my $count = $num =~ s/(.)/$1/sg;
    if ($count > 1) {
        my $sum;
        $sum += $_ for split(//,$num);
        print "sum=$sum\n";
        recur($sum);
    }
    else {
        print "$num";
    }
}

recur($number);


