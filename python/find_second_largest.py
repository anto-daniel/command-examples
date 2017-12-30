if __name__ == '__main__':
    n = int(raw_input())
    arr = map(int, raw_input().split())
    arr.sort()
    print arr
    arr.reverse()
    print arr
    newarr = list(set(arr))
    newarr.reverse()
    print newarr[1]
