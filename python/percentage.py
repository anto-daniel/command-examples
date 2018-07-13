if __name__ == '__main__':
    n = int(raw_input())
    student_marks = {}
    for _ in range(n):
        line = raw_input().split()
        name, scores = line[0], line[1:]
        scores = map(float, scores)
        student_marks[name] = scores
    print("Enter the name of the student to know the score")
    query_name = raw_input()
    a = sum(student_marks[query_name])/3
    print("%.2f" % a)
