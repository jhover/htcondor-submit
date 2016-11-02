#!/usr/bin/python
#
# Test and diagnostic script for mpi4py under HTCondor
# 
# John Hover <jhover@bnl.gov>
import glob
import logging
import os
import socket
import sys
import time

from os import path

# Add mpich to python path, and setup logging.
major, minor, release, st, num = sys.version_info
sys.path.append('/usr/lib64/python%s.%s/site-packages/mpich' % (major, minor))

# Defaults
default_logfile = "mpi_test.log"

# Logging
FORMATSTR = "[%(levelname)s] %(asctime)s %(module)s.%(funcName)s(): %(message)s"
log = logging.getLogger()
#hdlr = logging.StreamHandler(sys.stdout)
hdlr = logging.FileHandler(default_logfile)
formatter = logging.Formatter(FORMATSTR)
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG) # Override with command line switches
log.debug("Logging initialized.") 

try:
    from mpi4py import MPI
except ImportError:
    print("mpi4py not installed. Exitting.")
    sys.exit(1)

log.debug("__CONDOR_SCRATCH_DIR=%s" % os.environ.get("_CONDOR_SCRATCH_DIR", None))
cwd = os.getcwd()
hostname = socket.getfqdn()
log.debug(glob.glob("~/*"))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

log.debug("Hello world from node %d ( %d total ): %s" % (rank, size, str(glob.glob("*"))))

comm.Barrier()   # wait for everybody to synchronize _here_
