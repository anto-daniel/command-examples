#!/usr/bin/python

arr = []

N = int(raw_input())

for i in range(N):
    a = raw_input()
    if "insert" in a:
        arr.insert(int(a.split()[1]), int(a.split()[2]))
    elif "remove" in a:
        arr.remove(int(a.split()[1]))
    elif "append" in a:
        arr.append(int(a.split()[1]))
    elif "sort" in a:
        arr.sort()
    elif "print" in a:
        print arr
    elif "pop" in a:
        arr.pop()
    elif "reverse" in a:
        arr.reverse()
    else:
        continue
