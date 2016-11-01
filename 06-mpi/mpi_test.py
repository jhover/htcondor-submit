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

print "__CONDOR_SCRATCH_DIR=%s" % os.environ.get("_CONDOR_SCRATCH_DIR", None)
cwd = os.getcwd()
hostname = socket.getfqdn()
print glob.glob("~/*")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print "Hello world from node %d ( %d total ): %s" % (rank, size, str(glob.glob("*")))

comm.Barrier()   # wait for everybody to synchronize _here_

    
