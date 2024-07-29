#!/bin/bash

python ../generate.py --func_name $1 --dataset $2 --n $3

#python ../generate.py --func_name "opt" --dataset 2016 --n 3 --mem_kb 50 100 200 300 400

python ../generate.py --func_name $1 --dataset $2 --n $3 --mem_kb 50 100 200 300 400