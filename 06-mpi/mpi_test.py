#!/usr/bin/python

import os
from os import path

import sys
sys.path.append('/usr/lib64/python2.7/site-packages/mpich')

import time

from mpi4py import MPI
import glob

print os.environ.get("_CONDOR_SCRATCH_DIR", None)
cwd = os.getcwd()
os.makedirs("x/y/z")
os.chdir("x/y/z")
print glob.glob("/home/ahe/*")
print glob.glob("*")
os.chdir(cwd)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print "Hello from node %d ( %d ): %s" % (rank, size, str(glob.glob("*")))
os.makedirs("{}".format(size))
print "Hello from node %d ( %d ): %s" % (rank, size, str(glob.glob("*")))

if rank == 0:
    time.sleep(3)
    for rt,dirs,files in os.walk(cwd):
        for f in dirs + files:
            print path.join(rt, f)
