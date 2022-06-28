
from pip import main


import kaloot

import sys

def main():
    """Main function"""
    master = kaloot.calendar.Calendar()
    for d in master.iter_month_dates(1):
        print(d)

    # import timeit
    # N = 100000
    # setup = "import kaloot; master = kaloot.calendar.Calendar()"
    # print(timeit.timeit("for _ in master.iter_month_dates(1): pass", setup=setup, number=N))
    # print(timeit.timeit("for _ in master.iter_month_dates2(1): pass", setup=setup, number=N))



if __name__ == "__main__":
    sys.exit(main())
