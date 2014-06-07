#!/usr/bin/perl


$firstname = "Dean";  # Lexical Variable
@carmanufacturers = ("Honda", "Toyota", "Nissan", "Lexus", "BMW");

print "Hello $firstname. Please choose a car manufacturer\n";
print "@carmanufacturers[0..4]\n";
print "The final element is $#carmanufacturers\n";
