#!/usr/bin/python
#
# Test and diagnostic script for mpi4py under HTCondor
# 
# John Hover <jhover@bnl.gov>
import glob
import os
import socket
import sys
import time

from os import path

# Add mpich to python path...  
major, minor, release, st, num = sys.version_info
sys.path.append('/usr/lib64/python%s.%s/site-packages/mpich' % (major, minor))
try:
    from mpi4py import MPI
except ImportError:
    print("mpi4py not installed. Exitting.")
    sys.exit(1)

print os.environ.get("_CONDOR_SCRATCH_DIR", None)
cwd = os.getcwd()
hostname = socket.getfqdn()
#os.makedirs("x/y/z")
#os.chdir("x/y/z")
print glob.glob("~/*")
#print glob.glob("*")
#os.chdir(cwd)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print "Hello from node %d ( %d ): %s" % (rank, size, str(glob.glob("*")))
#os.makedirs("{}".format(size))
print "Hello from node %d ( %d ): %s" % (rank, size, str(glob.glob("*")))

if rank == 0:
    time.sleep(300)
    print "Node %s is controller..." % hostname 
    for rt,dirs,files in os.walk(cwd):
        for f in dirs + files:
            print path.join(rt, f)
else:
    time.sleep(300)
    print "Node %s is slave..." % hostname 
    for rt,dirs,files in os.walk(cwd):
        for f in dirs + files:
            print path.join(rt, f)    
    
