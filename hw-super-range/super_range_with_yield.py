def super_range(i):
    counter = 0
    while i > counter:
        yield counter
        counter += 1


if __name__ == "__main__":
    for x in super_range(100):
        print(x)
