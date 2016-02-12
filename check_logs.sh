#!/bin/bash

cd logs
SNAPSHOT=$(cat *  | awk -F " " '{print $1}' | sort -n| tail -n1)

for i in `seq 1 $SNAPSHOT`;
do
    echo $i
    cat * | awk -F " " -v conta=0 -v i=$i '{ if($1==i){ conta = conta + $2 + $3; }}END{print conta;}'
done
