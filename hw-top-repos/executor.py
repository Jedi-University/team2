import sys

from fetch import fetch
from show import show

if __name__ == "__main__":
    executor = {"fetch": fetch, "show": show}
    if len(sys.argv) == 2:
        executor.get(sys.argv[1], lambda: print("This command is undefined"))()
    else:
        print("No parameters found or too many parameters!")
