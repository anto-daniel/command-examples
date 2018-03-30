#!/usr/bin/python 
import sys

def rep(n):
    try:
        while n > 9:
            s = 0
            while n:
                s += n % 10
                n /= 10
            print s
            rep(s)
    except (FloatingPointError, ZeroDivisionError, OverflowError, ArithmeticError):
        print "Number less than 10: %d"

print rep(int(sys.argv[1]))
