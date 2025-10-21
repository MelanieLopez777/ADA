def fibonacci_r(n):

    if n<= 0:
        print("Incorrect input")

    elif n == 1:
        return 0

    elif n == 2:
        return 1
    else:
        return fibonacci_r(n-1)+fibonacci_r(n-2)


def fibonacci_dp(n):

    a = 0
    b = 1
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n + 1):
            c = a + b
            a = b
            b = c
        return b

