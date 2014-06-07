#!/usr/bin/perl -w

$make = "Toyota";
$firstname = "Dean";  # This is a scalar variable
@fullname = ("Dean", "Andrew", "Davis"); # This is an Array

%make_model = ("Honda", "Accord", "Toyota", "Camry"); # This is a Hash

	print "$make makes the: ";
	print $make_model{"$make"}, "\n";	
