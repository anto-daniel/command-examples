if __name__ == '__main__':
    n = int(raw_input())
    arr = map(int, raw_input().split())
    arr.sort()
    used = []
    unique = [x for x in arr if x not in used and used.append(x)]
    used.reverse()
    print used[1]
