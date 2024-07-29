#!/bin/bash

memTest=(50 100 200 300 400)

for i in ${memTest[@]}
do
    echo $i
    ./run_rskt.sh $i 64
done