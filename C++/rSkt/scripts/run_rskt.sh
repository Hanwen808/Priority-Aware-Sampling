#!/bin/bash

# options
optimize_flag="-O3"

# compile
echo "Compiling rSkt with $optimize_flag optimization flag..."
g++ ../Sources/rSkt.cpp ../Sources/MurmurHash3.cpp ../rSkt_main.cpp -o rskt -std=c++17 -I ../C++ $optimize_flag

if [ $? -eq 0 ]; then
    echo "Compilation successful. Running rskt..."
    ./rskt -total_mem $1 -v $2
    rm -rf ./rskt
else
    echo "Compilation failed. Exiting."
    exit 1
fi