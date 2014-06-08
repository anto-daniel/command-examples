#!/usr/bin/perl 

$player = "Sharapova";
%player_country = (
    Venus => "USA",
    Sharapova => "Russia",
    Serena => "USA",
);

    print "$player represents: ";
    print $player_country{"$player"};
    print "\n";

@players = keys %player_country;
@values = values %player_country;

    print "@players[0..$#players] \n";
    print "@values[0..$#values] \n";
