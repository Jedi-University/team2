import itertools


def func1(x1,x2,x3):
    def func2(x):
        return [x+x1, x+x2, x+x3]
    return func2


def unlist(x):
    if len(x)>1:
        x[0] = list(itertools.chain(x[0], x.pop(1)))
        x = unlist(x)
    else:
        return(x[0])
    return(x)


def a(x,y):
    global x1, y1
    print(f"{x1}{x} - {y1}{y}")


def caller(func, c, j):
    global x1
    global y1
    
    x1+=c
    y1+=j
    return func
    

while True:
    inp = input()
    if inp == "1":
        #1. дан следующий код

        f = func1("a", "b", "c")
        print(f("x"))

        '''Результат должен быть
        ["xa", "xb", "xc"]'''
    elif inp == "2":
        #2. дан лист листов
        l = [[1,2,3,4,5,6], [0,0,0,0], ["a", "b", "c"]]
        #print(list(itertools.chain.from_iterable(l)))
        l=unlist(l)
        print(l)
        '''Необходимо написать код который превратит его в простой лист 
        [1,2,3,4,5,6,0,0,0,0,"a", "b", "c"]
        для решения данной задачи нельзя использовать доп массива'''
    elif inp == "3":
        #3. написать реализацию метода caller
        x1, y1 = '', ''
        f = caller(a, "100", "200")
        f("h", "z")
        '''Результат
        "100h - 200z"'''
    else:
        exit() 
