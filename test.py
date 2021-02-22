import multiprocessing as mp


def my_f2(x):
    return(x**2)


# set the number of processes to be used
# # np = mp.cpu_count()   # ... as detected by multiprocessing
# NP = int(sys.argv[1])   # ... as passed in via the command line
NP = 2

with mp.Pool(NP) as p:
    output = p.starmap_async(my_f2, range(10))
    print(output.get())
