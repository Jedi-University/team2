import time


def calc_exec_time(min=False):
    def _calc_exec_time(function):
        def wrapper(*args, **kwargs):
            print(f"Function name: {function.__name__}")
            start = time.time()
            res = function(*args, **kwargs)
            end = time.time()
            total = (end - start) / 60 if min else end - start
            units_of_time = "min." if min else "sec."
            print(f"Function execution time: {total} {units_of_time}\n")
            return res
        return wrapper
    return _calc_exec_time


@calc_exec_time()
def a(x, y):
    print(f"{x} - {y}")


@calc_exec_time(min=False)
def sequence_square(limit):
    for i in range(1, limit):
        print(i ** 10, end=" ")
    print()


@calc_exec_time(min=True)
def fibonacci(n):
    n -= 2
    fib1 = fib2 = 1
    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1
    return fib2


if __name__ == '__main__':
    a(10, 10)
    sequence_square(1000)

    number = 3999999
    fibonacci_number = fibonacci(3999999)
    print(f"the {number} fibonacci number is {fibonacci_number}")
