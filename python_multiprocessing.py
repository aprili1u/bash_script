#!/usr/bin/env python

# import os, sys
# import multiprocessing as mp

def my_f(x):
  """Function to be run in parallel.
  """
#  print("{} : {}".format(x, os.getpid())) 
  print("Hello Word")

# set the number of processes to be used
#np = mp.cpu_count()   # ... as detected by multiprocessing
# np = int(sys.argv[1])   # ... as passed in via the command line

# with mp.Pool(np) as p:
#   p.map(my_f, range(np))
