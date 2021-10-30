def super_range(i):
  n=0
  while n<i:
    yield n
    n=n+1


for x in super_range(100):
  print(x)