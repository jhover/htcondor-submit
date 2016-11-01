#!/bin/sh
##**************************************************************
##
## Copyright (C) 1990-2012, Condor Team, Computer Sciences Department,
## University of Wisconsin-Madison, WI.
## 
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License.  You may
## obtain a copy of the License at
## 
##    http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Modified by John Hover <jhover@bnl.gov> for extra debug info...
##
##**************************************************************

echo "Starting job wrapper... "

_CONDOR_PROCNO=$_CONDOR_PROCNO
_CONDOR_NPROCS=$_CONDOR_NPROCS

CONDOR_SSH=`condor_config_val libexec`
CONDOR_SSH=$CONDOR_SSH/condor_ssh

SSHD_SH=`condor_config_val libexec`
SSHD_SH=$SSHD_SH/sshd.sh

echo "Parameters: "
echo "_CONDOR_PROCNO=$_CONDOR_PROCNO"
echo "_CONDOR_NPROCS=$_CONDOR_NPROCS"
echo "CONDOR_SSH=$CONDOR_SSH"
echo "SSHD_SH=$SSHD_SH/sshd.sh"

echo "Executing SSHD startup..."
echo ". $SSHD_SH $_CONDOR_PROCNO $_CONDOR_NPROCS"

. $SSHD_SH $_CONDOR_PROCNO $_CONDOR_NPROCS 

# If not the head node, just sleep forever, to let the
# sshds run
if [ $_CONDOR_PROCNO -ne 0 ]
then
		echo "_CONDOR_PROCNO != 0, waiting..."
		wait
		sshd_cleanup
		exit 0
fi

EXECUTABLE=$1
shift

# the binary is copied but the executable flag is cleared.
# so the script have to take care of this
chmod +x $EXECUTABLE

echo "_CONDOR_PROCNO == 0, Handling executable $EXECUTABLE"

# Set this to the bin directory of MPICH installation
MPDIR=/usr/lib64/mpich/bin
PATH=$MPDIR:.:$PATH
export PATH

export P4_RSHCOMMAND=$CONDOR_SSH
export HYDRA_LAUNCHER_EXEC=$CONDOR_SSH

CONDOR_CONTACT_FILE=$_CONDOR_SCRATCH_DIR/contact
export CONDOR_CONTACT_FILE

echo "Contents of contact file $CONDOR_CONTACT_FILE"
cat $CONDOR_CONTACT_FILE

# The second field in the contact file is the machine name
# that condor_ssh knows how to use
sort -n -k 1 < $CONDOR_CONTACT_FILE | awk '{print $2}' > machines

echo "Contents of machine file:"
cat machines

## run the actual mpijob

echo "Running mpirun -verbose -np $_CONDOR_NPROCS -machinefile machines $EXECUTABLE $@"
mpirun -verbose -np $_CONDOR_NPROCS -machinefile machines $EXECUTABLE $@ 2>&1

echo "mpirun done. Performing ssh_cleanup..."

sshd_cleanup
rm -f machines

echo "Job completed. Exitting"

exit $?
