#!/bin/env bash
echo "****************************************"
date 
whoami
id
hostname
env | sort
echo "Staging in input data"

echo "Running jobs"
crb-blast --query Creinhardtii.fa --target Athaliana.fa --output output1.tsv
echo "Staging output"
date
echo "****************************************"
