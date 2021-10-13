import itertools


def func(x1,x2,x3):
    def func1(x):
        return [x+x1, x+x2, x+x3]
    return func1


def unlist(x):
    if len(x)>1:
        x[0] = list(itertools.chain(x[0], x.pop(1)))
        x = unlist(x)
    else:
        return(x[0])
    return(x)


while True:
    a = input()
    if a == "1":
        #1. дан следующий код

        f = func("a", "b", "c")
        print(f("x"))

        '''Результат должен быть
        ["xa", "xb", "xc"]'''
    elif a == "2":
        print(2)
        #2. дан лист листов
        l = [[1,2,3,4,5,6], [0,0,0,0], ["a", "b", "c"]]
        #print(list(itertools.chain.from_iterable(l)))
        l=unlist(l)
        print(l)
        '''Необходимо написать код который превратит его в простой лист 
        [1,2,3,4,5,6,0,0,0,0,"a", "b", "c"]
        для решения данной задачи нельзя использовать доп массива'''
    else:
        exit()
