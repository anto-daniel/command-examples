#!/usr/bin/python

arr = []

N = int(raw_input())

for i in range(N):
    a = raw_input()
    if "insert" in a:
        arr.insert(int(a.split()[1]), int(a.split()[2]))
    if "remove" in a:
        arr.remove(int(a.split()[1]))
    if "append" in a:
        arr.append(int(a.split()[1]))
    if "sort" in a:
        arr.sort()
    if "print" in a:
        print arr
    if "pop" in a:
        arr.pop()
    if "reverse" in a:
        arr.reverse()
