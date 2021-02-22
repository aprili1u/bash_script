# import multiprocessing as mp


# def my_f2(x):
#     return(x**2)


# # set the number of processes to be used
# # # np = mp.cpu_count()   # ... as detected by multiprocessing
# # NP = int(sys.argv[1])   # ... as passed in via the command line
# def main():
#     NP = 2

#     with mp.Pool(NP) as p:
#         output = p.starmap_async(my_f2, range(10))
#         print(output.get())


# if __name__ == "__main__":
#     main()
# import multiprocessing as mp
# import time


# def f(x):
#     print(x*x)


# if __name__ == '__main__':
#     with mp.Pool(4) as p:
#         r = p.map_async(f, range(10))
#     # DO STUFF
#     print('HERE')
#     print('MORE')
#     r.wait()
#     print('DONE')
from multiprocessing import Pool


def func(x):
    return (x**2)


if __name__ == '__main__':
    pool = Pool(processes=4)
    r = pool.map_async(func, range(10))
    print(r.get())
