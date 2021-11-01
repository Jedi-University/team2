'''
декоратор который может считать время выполнения функции и выводить его в консоль, 
нужно сделать возможным передать min=True/False, что позволят выводить время в минутах в случае True и в секундах в случае False
'''

from time import sleep
import datetime as d

def logger(**kwargs):
  is_min = kwargs.get('min',False)
  def wrapper(f):
    def wrapped_function(*args,**kwargs):
      s=d.datetime.today()
      print("start logging")
      f(**kwargs)
      dl=(d.datetime.today()-s)/60 if is_min else (d.datetime.today()-s)
      print(dl.total_seconds(), ('min' if is_min else 'sec'))
    return wrapped_function
  return wrapper

@logger(min=False)
def f(t):
  for i in range(t):
    sleep(1)


### test it ###

f(t=1)