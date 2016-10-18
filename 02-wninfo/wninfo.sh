#!/bin/env bash
echo "****************************************"
date 
whoami
id
hostname
env | sort
which condor_config_val
condor_config_val -dump | sort
sleep 5
date
echo "****************************************"
