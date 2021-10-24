def decor(f):
    def wrap(x, *args):
        for arg in args:
            f(x, arg)
    return(wrap)


@decor
def func(*args):
    string = ''.join(str(a) for a in args)
    print(string, end=',')
    

func('x', 1, 4, 2, 's', 'Saratov')