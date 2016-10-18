#!/bin/env bash
echo "*********START*************************"
date
echo "*********NODE*************************"
hostname
echo "*********JOB*************************"
echo "Running job.."
echo "Args are $@"
echo "cat $1 | grep epel > $2"
cat $1 | grep epel > $2
RET=$?
date
echo "Return code was $RET"
sleep 30
echo "*********DONE***************************"
exit $RET
