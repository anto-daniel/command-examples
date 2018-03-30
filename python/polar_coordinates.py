# Enter your code here. Read input from STDIN. Print output to STDOUT
from __future__ import print_function
from cmath import phase
from cmath import polar

if __name__ == "__main__":
    a = input()
    c = phase(a)
    d = abs(a)
    print(d)
    print(c)
