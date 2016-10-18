#!/bin/env bash
echo "*********START*************************"
date
echo "*********NODE*************************"
hostname
echo "*********JOB*************************"
echo "Uncompressing software..."
tar -xvzf mysoft.tgz
chmod +x bin/*
export PATH=$PATH:`pwd`/bin
echo $PATH
which filterepel.sh
echo "Running job.."
echo "filterepel.sh $@"
filterepel.sh $@
RET=$?
date
echo "Return code was $RET"
sleep 30
echo "*********DONE***************************"
exit $RET
