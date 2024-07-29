#!/bin/bash
probs2016=(0.1 0.33 0.574 0.691 0.758)
probs2019=(0.013 0.116 0.341 0.488 0.584)
mems=(50 100 200 300 400)
prior=(3 7)
dataset=(2016 2019)
highs=("H=(3)" "H=(6 7)")
lows=("L=(1 2)" "L=(1 2 3 4 5)")

for _prior in "${prior[@]}"
do
    high_array=("${highs[@]}")
    low_array=("${lows[@]}")
    if [ $_prior -eq 3 ] ; then
        param_high="${high_array[0]}"
        param_low="${low_array[0]}"
    elif [ $_prior -eq 7 ] ; then
        param_high="${high_array[1]}"
        param_low="${low_array[1]}"
    fi
    eval $param_high
    eval $param_low
    for _dataset in "${dataset[@]}"
    do
        for i in $(seq 0 4) 
        do
            if [ ${_dataset} -eq 2016 ] ; then
                #echo "NDS(${_dataset},${_prior},p=${probs2016[$i]},mem=${mems[$i]},high=$H, low=$L) is running..."
                if [ $_prior -eq 3 ] ; then
                    python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
                elif [ $_prior -eq 7 ] ; then
                    python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
                fi
                 
            else
                #echo "NDS(${_dataset},${_prior},p=${probs2019[$i]},mem=${mems[$i]},high=$H, low=$L) is running..."
                if [ $_prior -eq 3 ] ; then
                    python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2019[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
                elif [ $_prior -eq 7 ] ; then
                    python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2019[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
                fi
            fi
        done
    done
done

