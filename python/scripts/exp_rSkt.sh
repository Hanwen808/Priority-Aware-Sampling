#!/bin/bash
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
                #echo "vHLL(${_dataset},${_prior},mem=${mems[$i]}) is running..."
                if [ $_prior -eq 3 ] ; then
                    python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
                elif [ $_prior -eq 7 ] ; then
                    python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
                fi
            else
                if [ $_prior -eq 3 ] ; then
                    python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
                elif [ $_prior -eq 7 ] ; then
                    python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
                fi
            fi
        done
    done
done

