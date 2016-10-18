#!/bin/bash
echo "Finding epel packages in list..."
cat $1 | grep epel > $2
echo "Done"

