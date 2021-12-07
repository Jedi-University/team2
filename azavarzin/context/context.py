# 1. дан следующий код
# f = func("a", "b", "c")
# print(f("x"))
# Результат должен быть
# ["xa", "xb", "xc"]
from functools import reduce


def func(a, b, c):
    return lambda x: [x + a, x + b, x + c]


# 2. дан лист листов
# l = [[1,2,3,4,5,6], [0,0,0,0], ["a", "b", "c"]]
# Необходимо написать код который превратит его в простой лист
# [1,2,3,4,5,6,0,0,0,0,"a", "b", "c"]
# для решения данной задачи нельзя использовать доп массива
join_list_of_lists_into_list = lambda l: reduce(lambda a, b: a + b, l)


# 3. написать реализацию метода caller
# результат: "100h - 200z"
def a(x, y):
    print(f"{x} - {y}")


def caller(func, c, j):
    return lambda a, b: func(c + a, j + b)


if __name__ == "__main__":
    # task 1
    f = func("a", "b", "c")
    print(f("x"))

    # task 2
    l = [[1, 2, 3, 4, 5, 6], [0, 0, 0, 0], ["a", "b", "c"]]
    print(join_list_of_lists_into_list(l))

    # task 3
    f = caller(a, "100", "200")
    f("h", "z")
